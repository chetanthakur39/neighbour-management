package com.neighbourmanagement.backend.service.impl;

import com.neighbourmanagement.backend.dto.AutomationCreateRequest;
import com.neighbourmanagement.backend.dto.AutomationResponse;
import com.neighbourmanagement.backend.entity.Automation;
import com.neighbourmanagement.backend.entity.AutomationRule;
import com.neighbourmanagement.backend.enums.AutomationRuleType;
import com.neighbourmanagement.backend.enums.AutomationStatus;
import com.neighbourmanagement.backend.repository.AutomationExecutionRepository;
import com.neighbourmanagement.backend.repository.AutomationRepository;
import com.neighbourmanagement.backend.repository.AutomationRuleRepository;
import com.neighbourmanagement.backend.service.AutomationService;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class AutomationServiceImpl
        implements AutomationService {

    private final AutomationRepository automationRepository;

    private final AutomationRuleRepository automationRuleRepository;

    private final AutomationExecutionRepository automationExecutionRepository;


    // =========================================================
    // CONSTRUCTOR
    // =========================================================

    public AutomationServiceImpl(
            AutomationRepository automationRepository,
            AutomationRuleRepository automationRuleRepository,
            AutomationExecutionRepository automationExecutionRepository
    ) {

        this.automationRepository =
                automationRepository;

        this.automationRuleRepository =
                automationRuleRepository;

        this.automationExecutionRepository =
                automationExecutionRepository;
    }


    // =========================================================
    // CREATE AUTOMATION
    // =========================================================

    @Override
    @Transactional
    public AutomationResponse createAutomation(
            AutomationCreateRequest request
    ) {

        if (request == null) {

            throw new IllegalArgumentException(
                    "Automation request cannot be null"
            );
        }


        // =====================================================
        // BASIC VALIDATION
        // =====================================================

        if (
                request.getState() == null
                        || request.getState().trim().isEmpty()
        ) {

            throw new IllegalArgumentException(
                    "State is required to create automation"
            );
        }


        if (
                request.getJc() == null
                        || request.getJc().trim().isEmpty()
        ) {

            throw new IllegalArgumentException(
                    "JC is required to create automation"
            );
        }


        if (
                request.getExecutionTime() == null
        ) {

            throw new IllegalArgumentException(
                    "Execution time is required to create automation"
            );
        }


        // =====================================================
        // CREATE AUTOMATION ENTITY
        // =====================================================

        Automation automation =
                new Automation();


        // =====================================================
        // AUTOMATION NAME
        //
        // Chatbot may not provide a name.
        //
        // In that case generate a safe default name.
        //
        // Example:
        //
        // Neighbour Cleanup - Maharashtra - JC_Mumbai
        //
        // This prevents:
        //
        // Column 'name' cannot be null
        // =====================================================

        String automationName =
                request.getName();


        if (
                automationName == null
                        || automationName.trim().isEmpty()
        ) {

            automationName =
                    "Neighbour Cleanup - "
                            + request.getState()
                            + " - "
                            + request.getJc();
        }


        automation.setName(
                automationName
        );


        // =====================================================
        // STATE
        // =====================================================

        automation.setState(
                request.getState()
        );


        // =====================================================
        // JC
        // =====================================================

        automation.setJc(
                request.getJc()
        );


        // =====================================================
        // TECHNOLOGY FLOW
        // =====================================================

        automation.setTechnologyFlow(
                request.getTechnologyFlow()
        );


        // =====================================================
        // EXECUTION TIME
        // =====================================================

        automation.setExecutionTime(
                request.getExecutionTime()
        );


        // =====================================================
        // MINIMUM NEIGHBOURS
        // =====================================================

        automation.setMinimumNeighbours(
                request.getMinimumNeighbours()
        );


        // =====================================================
        // STATUS
        // =====================================================

        automation.setStatus(
                AutomationStatus.RUNNING
        );


        // =====================================================
        // CALCULATE FIRST NEXT RUN
        // =====================================================

        LocalDateTime now =
                LocalDateTime.now();


        automation.setNextRunAt(
                calculateNextRun(
                        automation,
                        now
                )
        );


        // =====================================================
        // SAVE AUTOMATION
        // =====================================================

        Automation savedAutomation =
                automationRepository.save(
                        automation
                );


        // =====================================================
        // SAVE AUTOMATION RULES
        // =====================================================

        if (
                request.getRules() != null
                        && !request.getRules().isEmpty()
        ) {

            for (
                    AutomationRuleType ruleType
                    : request.getRules()
            ) {

                AutomationRule rule =
                        new AutomationRule();


                rule.setAutomation(
                        savedAutomation
                );


                rule.setRuleType(
                        ruleType
                );


                rule.setEnabled(
                        true
                );


                automationRuleRepository.save(
                        rule
                );
            }
        }


        // =====================================================
        // RETURN RESPONSE
        // =====================================================

        return toResponse(
                savedAutomation
        );
    }


    // =========================================================
    // GET ALL AUTOMATIONS
    // =========================================================

    @Override
    @Transactional(readOnly = true)
    public List<AutomationResponse> getAllAutomations() {

        return automationRepository
                .findAll()
                .stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
    }


    // =========================================================
    // GET AUTOMATION BY ID
    // =========================================================

    @Override
    @Transactional(readOnly = true)
    public AutomationResponse getAutomationById(
            Long automationId
    ) {

        Automation automation =
                automationRepository
                        .findById(
                                automationId
                        )
                        .orElseThrow(
                                () -> new IllegalArgumentException(
                                        "Automation not found: "
                                                + automationId
                                )
                        );


        return toResponse(
                automation
        );
    }


    // =========================================================
    // PAUSE AUTOMATION
    // =========================================================

    @Override
    @Transactional
    public AutomationResponse pauseAutomation(
            Long automationId
    ) {

        Automation automation =
                getAutomation(
                        automationId
                );


        if (
                automation.getStatus()
                        == AutomationStatus.ENDED
        ) {

            throw new IllegalStateException(
                    "Ended automation cannot be paused"
            );
        }


        automation.setStatus(
                AutomationStatus.PAUSED
        );


        automation.setPausedAt(
                LocalDateTime.now()
        );


        // No scheduled execution while paused.

        automation.setNextRunAt(
                null
        );


        Automation saved =
                automationRepository.save(
                        automation
                );


        return toResponse(
                saved
        );
    }


    // =========================================================
    // RESUME AUTOMATION
    // =========================================================

    @Override
    @Transactional
    public AutomationResponse resumeAutomation(
            Long automationId
    ) {

        Automation automation =
                getAutomation(
                        automationId
                );


        if (
                automation.getStatus()
                        == AutomationStatus.ENDED
        ) {

            throw new IllegalStateException(
                    "Ended automation cannot be resumed"
            );
        }


        automation.setStatus(
                AutomationStatus.RUNNING
        );


        automation.setPausedAt(
                null
        );


        if (
                automation.getStartedAt() == null
        ) {

            automation.setStartedAt(
                    LocalDateTime.now()
            );
        }


        // Calculate next scheduled execution.

        automation.setNextRunAt(
                calculateNextRun(
                        automation,
                        LocalDateTime.now()
                )
        );


        Automation saved =
                automationRepository.save(
                        automation
                );


        return toResponse(
                saved
        );
    }


    // =========================================================
    // END AUTOMATION
    // =========================================================

    @Override
    @Transactional
    public AutomationResponse endAutomation(
            Long automationId
    ) {

        Automation automation =
                getAutomation(
                        automationId
                );


        automation.setStatus(
                AutomationStatus.ENDED
        );


        automation.setEndedAt(
                LocalDateTime.now()
        );


        // No future execution.

        automation.setNextRunAt(
                null
        );


        Automation saved =
                automationRepository.save(
                        automation
                );


        return toResponse(
                saved
        );
    }


    // =========================================================
    // DELETE AUTOMATION
    // =========================================================

    @Override
    @Transactional
    public void deleteAutomation(
            Long automationId
    ) {

        Automation automation =
                getAutomation(
                        automationId
                );


        // -----------------------------------------------------
        // 1. Delete execution history first
        // -----------------------------------------------------

        automationExecutionRepository
                .deleteByAutomation_AutomationId(
                        automationId
                );


        // Make sure execution deletes are flushed
        // before deleting the parent automation.

        automationExecutionRepository.flush();


        // -----------------------------------------------------
        // 2. Delete automation rules
        // -----------------------------------------------------

        automationRuleRepository
                .deleteByAutomationId(
                        automationId
                );


        // Make sure rule deletes are flushed
        // before deleting the parent automation.

        automationRuleRepository.flush();


        // -----------------------------------------------------
        // 3. Delete automation
        // -----------------------------------------------------

        automationRepository.delete(
                automation
        );


        // Flush the parent delete.

        automationRepository.flush();
    }


    // =========================================================
    // GET AUTOMATION
    // =========================================================

    private Automation getAutomation(
            Long automationId
    ) {

        return automationRepository
                .findById(
                        automationId
                )
                .orElseThrow(
                        () -> new IllegalArgumentException(
                                "Automation not found: "
                                        + automationId
                        )
                );
    }


    // =========================================================
    // CALCULATE NEXT RUN
    // =========================================================

    private LocalDateTime calculateNextRun(
            Automation automation,
            LocalDateTime now
    ) {

        // -----------------------------------------------------
        // Currently only DAILY is supported.
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
        // Execution time must exist.
        // -----------------------------------------------------

        LocalTime executionTime =
                automation.getExecutionTime();


        if (executionTime == null) {

            return null;
        }


        // -----------------------------------------------------
        // Today's scheduled time.
        // -----------------------------------------------------

        LocalDateTime todayRun =
                LocalDateTime.of(
                        LocalDate.now(),
                        executionTime
                );


        // -----------------------------------------------------
        // If today's time has not passed,
        // schedule for today.
        // -----------------------------------------------------

        if (
                todayRun.isAfter(now)
        ) {

            return todayRun;
        }


        // -----------------------------------------------------
        // Otherwise schedule for tomorrow.
        // -----------------------------------------------------

        return todayRun.plusDays(1);
    }


    // =========================================================
    // ENTITY → RESPONSE
    // =========================================================

    private AutomationResponse toResponse(
            Automation automation
    ) {

        AutomationResponse response =
                new AutomationResponse();


        // -----------------------------------------------------
        // Basic automation fields
        // -----------------------------------------------------

        response.setAutomationId(
                automation.getAutomationId()
        );

        response.setName(
                automation.getName()
        );

        response.setState(
                automation.getState()
        );

        response.setJc(
                automation.getJc()
        );

        response.setTechnologyFlow(
                automation.getTechnologyFlow()
        );


        // -----------------------------------------------------
        // Frequency
        // -----------------------------------------------------

        response.setFrequency(
                automation.getFrequency()
        );


        // -----------------------------------------------------
        // Execution configuration
        // -----------------------------------------------------

        response.setExecutionTime(
                automation.getExecutionTime()
        );

        response.setMinimumNeighbours(
                automation.getMinimumNeighbours()
        );


        // -----------------------------------------------------
        // Status
        // -----------------------------------------------------

        response.setStatus(
                automation.getStatus()
        );


        // -----------------------------------------------------
        // Execution times
        // -----------------------------------------------------

        response.setLastRunAt(
                automation.getLastRunAt()
        );

        response.setNextRunAt(
                automation.getNextRunAt()
        );


        // -----------------------------------------------------
        // Created time
        // -----------------------------------------------------

        response.setCreatedAt(
                automation.getCreatedAt()
        );


        // -----------------------------------------------------
        // Rules
        // -----------------------------------------------------

        List<AutomationRuleType> rules =
                automationRuleRepository
                        .findByAutomation_AutomationIdAndEnabledTrue(
                                automation.getAutomationId()
                        )
                        .stream()
                        .map(
                                AutomationRule::getRuleType
                        )
                        .collect(Collectors.toList());


        response.setRules(
                rules
        );


        return response;
    }
}