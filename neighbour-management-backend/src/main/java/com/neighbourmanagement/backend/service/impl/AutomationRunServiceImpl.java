package com.neighbourmanagement.backend.service.impl;

import com.neighbourmanagement.backend.dto.deletion.DeletionRequest;
import com.neighbourmanagement.backend.dto.safety.SafetyDecisionResponse;
import com.neighbourmanagement.backend.dto.validation.ValidationRequest;
import com.neighbourmanagement.backend.dto.validation.ValidationResponse;
import com.neighbourmanagement.backend.entity.Automation;
import com.neighbourmanagement.backend.entity.AutomationExecution;
import com.neighbourmanagement.backend.entity.AutomationRule;
import com.neighbourmanagement.backend.enums.AutomationRuleType;
import com.neighbourmanagement.backend.repository.AutomationRepository;
import com.neighbourmanagement.backend.repository.AutomationRuleRepository;
import com.neighbourmanagement.backend.service.AutomationExecutionService;
import com.neighbourmanagement.backend.service.AutomationRunService;
import com.neighbourmanagement.backend.service.DeletionService;
import com.neighbourmanagement.backend.service.SafetyService;
import com.neighbourmanagement.backend.service.ValidationService;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;

@Service
public class AutomationRunServiceImpl
        implements AutomationRunService {

    private final AutomationRepository
            automationRepository;

    private final AutomationRuleRepository
            automationRuleRepository;

    private final ValidationService
            validationService;

    private final SafetyService
            safetyService;

    private final DeletionService
            deletionService;

    private final AutomationExecutionService
            automationExecutionService;


    // =========================================================
    // CONSTRUCTOR
    // =========================================================

    public AutomationRunServiceImpl(
            AutomationRepository automationRepository,
            AutomationRuleRepository automationRuleRepository,
            ValidationService validationService,
            SafetyService safetyService,
            DeletionService deletionService,
            AutomationExecutionService automationExecutionService
    ) {

        this.automationRepository =
                automationRepository;

        this.automationRuleRepository =
                automationRuleRepository;

        this.validationService =
                validationService;

        this.safetyService =
                safetyService;

        this.deletionService =
                deletionService;

        this.automationExecutionService =
                automationExecutionService;
    }


    // =========================================================
    // RUN AUTOMATION
    // =========================================================

    @Override
    @Transactional
    public Object runAutomation(
            Long automationId
    ) {

        // =====================================================
        // 1. FIND AUTOMATION
        // =====================================================

        Automation automation =
                automationRepository
                        .findById(automationId)
                        .orElseThrow(
                                () -> new IllegalArgumentException(
                                        "Automation not found: "
                                                + automationId
                                )
                        );


        // =====================================================
        // 2. START EXECUTION
        // =====================================================

        AutomationExecution execution =
                automationExecutionService
                        .startExecution(
                                automationId
                        );


        try {

            // =================================================
            // 3. GET ENABLED RULES
            // =================================================

            List<AutomationRule> enabledRules =
                    automationRuleRepository
                            .findByAutomation_AutomationIdAndEnabledTrue(
                                    automationId
                            );


            // =================================================
            // 4. CONVERT RULES TO RULE TYPES
            // =================================================

            List<AutomationRuleType> rules =
                    enabledRules
                            .stream()
                            .map(
                                    AutomationRule::getRuleType
                            )
                            .filter(
                                    rule ->
                                            rule == AutomationRuleType.PCI
                                                    || rule == AutomationRuleType.TAC
                            )
                            .toList();


            // =================================================
            // 5. PCI/TAC RULE CHECK
            // =================================================

            if (rules.isEmpty()) {

                throw new IllegalArgumentException(
                        "Automation has no enabled PCI or TAC rules"
                );
            }


            // =================================================
            // 6. CREATE VALIDATION REQUEST
            // =================================================

            ValidationRequest validationRequest =
                    new ValidationRequest();

            validationRequest.setState(
                    automation.getState()
            );

            validationRequest.setJc(
                    automation.getJc()
            );

            validationRequest.setRules(
                    rules
            );


            // =================================================
            // 7. RUN VALIDATION
            // =================================================

            ValidationResponse validationResponse =
                    validationService.runValidation(
                            validationRequest
                    );


            // =================================================
            // 8. RUN SAFETY ENGINE
            // =================================================

            SafetyDecisionResponse safetyResponse =
                    safetyService.evaluate(
                            validationResponse,
                            automation.getMinimumNeighbours()
                    );


            // =================================================
            // 9. DELETE ONLY IF SAFETY ALLOWS
            // =================================================

            int deletedCount = 0;


            if (
                    safetyResponse.isDeletionAllowed()
                            && safetyResponse
                            .getNeighbourIdsToDelete() != null
                            && !safetyResponse
                            .getNeighbourIdsToDelete()
                            .isEmpty()
            ) {

                DeletionRequest deletionRequest =
                        new DeletionRequest();


                deletionRequest.setState(
                        automation.getState()
                );


                deletionRequest.setJc(
                        automation.getJc()
                );


                deletionRequest.setMinimumNeighbours(
                        automation.getMinimumNeighbours()
                );


                deletionRequest.setNeighbourIds(
                        safetyResponse
                                .getNeighbourIdsToDelete()
                );


                // =================================================
                // IMPORTANT:
                //
                // This deletion is marked as AUTOMATION.
                //
                // DeletionService will:
                //
                // 1. Verify State + JC + IDs
                // 2. Delete verified neighbours
                // 3. Record deletion_history
                // 4. Return deleted count
                // =================================================

                deletedCount =
                        deletionService.deleteNeighbours(
                                deletionRequest,
                                "AUTOMATION"
                        );
            }


            // =================================================
            // 10. COMPLETE AUTOMATION EXECUTION
            // =================================================

            automationExecutionService.completeExecution(
                    execution.getExecutionId(),
                    safetyResponse.getTotalNeighbours(),
                    safetyResponse.getValidNeighbours(),
                    safetyResponse.getInvalidNeighbours(),
                    deletedCount,
                    safetyResponse.getNeighboursToRetain()
            );


            // =================================================
            // 11. UPDATE LAST RUN
            // =================================================

            LocalDateTime now =
                    LocalDateTime.now();

            automation.setLastRunAt(
                    now
            );


            // =================================================
            // 12. CALCULATE NEXT RUN
            // =================================================

            LocalDateTime nextRunAt =
                    calculateNextRun(
                            automation,
                            now
                    );

            automation.setNextRunAt(
                    nextRunAt
            );


            // =================================================
            // 13. SAVE AUTOMATION
            // =================================================

            automationRepository.save(
                    automation
            );


            // =================================================
            // 14. RETURN SAFETY RESULT
            // =================================================

            return safetyResponse;


        } catch (Exception exception) {

            // =================================================
            // MARK EXECUTION AS FAILED
            // =================================================

            automationExecutionService.failExecution(
                    execution.getExecutionId(),
                    exception.getMessage()
            );

            throw exception;
        }
    }


    // =========================================================
    // CALCULATE NEXT RUN
    // =========================================================

    private LocalDateTime calculateNextRun(
            Automation automation,
            LocalDateTime now
    ) {

        // -----------------------------------------------------
        // CURRENTLY SUPPORT DAILY
        // -----------------------------------------------------

        if (
                automation.getFrequency() == null
                        || !"DAILY".equalsIgnoreCase(
                        automation.getFrequency()
                )
        ) {

            return null;
        }


        // -----------------------------------------------------
        // EXECUTION TIME
        // -----------------------------------------------------

        LocalTime executionTime =
                automation.getExecutionTime();

        if (executionTime == null) {

            return null;
        }


        // -----------------------------------------------------
        // TODAY'S SCHEDULED TIME
        // -----------------------------------------------------

        LocalDateTime todayRun =
                LocalDateTime.of(
                        LocalDate.now(),
                        executionTime
                );


        // -----------------------------------------------------
        // TODAY
        // -----------------------------------------------------

        if (todayRun.isAfter(now)) {

            return todayRun;
        }


        // -----------------------------------------------------
        // TOMORROW
        // -----------------------------------------------------

        return todayRun.plusDays(1);
    }
}