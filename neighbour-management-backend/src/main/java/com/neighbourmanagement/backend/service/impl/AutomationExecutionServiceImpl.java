package com.neighbourmanagement.backend.service.impl;

import com.neighbourmanagement.backend.entity.Automation;
import com.neighbourmanagement.backend.entity.AutomationExecution;
import com.neighbourmanagement.backend.enums.ExecutionStatus;
import com.neighbourmanagement.backend.repository.AutomationExecutionRepository;
import com.neighbourmanagement.backend.repository.AutomationRepository;
import com.neighbourmanagement.backend.service.AutomationExecutionService;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class AutomationExecutionServiceImpl
        implements AutomationExecutionService {

    private final AutomationRepository automationRepository;

    private final AutomationExecutionRepository
            automationExecutionRepository;


    public AutomationExecutionServiceImpl(
            AutomationRepository automationRepository,
            AutomationExecutionRepository automationExecutionRepository
    ) {
        this.automationRepository =
                automationRepository;

        this.automationExecutionRepository =
                automationExecutionRepository;
    }


    // =========================================================
    // START EXECUTION
    // =========================================================

    @Override
    @Transactional
    public AutomationExecution startExecution(
            Long automationId
    ) {

        Automation automation =
                automationRepository
                        .findById(automationId)
                        .orElseThrow(
                                () -> new IllegalArgumentException(
                                        "Automation not found: "
                                                + automationId
                                )
                        );


        AutomationExecution execution =
                new AutomationExecution();


        execution.setAutomation(
                automation
        );

        execution.setStartedAt(
                LocalDateTime.now()
        );

        execution.setState(
                automation.getState()
        );

        execution.setJc(
                automation.getJc()
        );

        execution.setTotalChecked(0);

        execution.setValidCount(0);

        execution.setInvalidCount(0);

        execution.setDeletedCount(0);

        execution.setRetainedCount(0);

        execution.setStatus(
                ExecutionStatus.RUNNING
        );

        execution.setErrorMessage(
                null
        );


        return automationExecutionRepository.save(
                execution
        );
    }


    // =========================================================
    // COMPLETE EXECUTION
    // =========================================================

    @Override
    @Transactional
    public AutomationExecution completeExecution(
            Long executionId,
            int totalChecked,
            int validCount,
            int invalidCount,
            int deletedCount,
            int retainedCount
    ) {

        AutomationExecution execution =
                automationExecutionRepository
                        .findById(executionId)
                        .orElseThrow(
                                () -> new IllegalArgumentException(
                                        "Execution not found: "
                                                + executionId
                                )
                        );


        execution.setTotalChecked(
                totalChecked
        );

        execution.setValidCount(
                validCount
        );

        execution.setInvalidCount(
                invalidCount
        );

        execution.setDeletedCount(
                deletedCount
        );

        execution.setRetainedCount(
                retainedCount
        );

        execution.setCompletedAt(
                LocalDateTime.now()
        );

        execution.setStatus(
                ExecutionStatus.SUCCESS
        );

        execution.setErrorMessage(
                null
        );


        return automationExecutionRepository.save(
                execution
        );
    }


    // =========================================================
    // FAILED EXECUTION
    // =========================================================

    @Override
    @Transactional
    public AutomationExecution failExecution(
            Long executionId,
            String errorMessage
    ) {

        AutomationExecution execution =
                automationExecutionRepository
                        .findById(executionId)
                        .orElseThrow(
                                () -> new IllegalArgumentException(
                                        "Execution not found: "
                                                + executionId
                                )
                        );


        execution.setCompletedAt(
                LocalDateTime.now()
        );

        execution.setStatus(
                ExecutionStatus.FAILED
        );

        execution.setErrorMessage(
                errorMessage
        );


        return automationExecutionRepository.save(
                execution
        );
    }


    // =========================================================
    // GET EXECUTIONS
    // =========================================================

    @Override
    @Transactional(readOnly = true)
    public List<AutomationExecution> getExecutions(
            Long automationId
    ) {

       return automationExecutionRepository
        .findByAutomation_AutomationIdOrderByStartedAtDesc(
                automationId
        );
    }
}