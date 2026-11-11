package com.neighbourmanagement.backend.service;

import com.neighbourmanagement.backend.entity.AutomationExecution;

import java.util.List;

public interface AutomationExecutionService {

    AutomationExecution startExecution(
            Long automationId
    );

    AutomationExecution completeExecution(
            Long executionId,
            int totalChecked,
            int validCount,
            int invalidCount,
            int deletedCount,
            int retainedCount
    );

    AutomationExecution failExecution(
            Long executionId,
            String errorMessage
    );

    List<AutomationExecution> getExecutions(
            Long automationId
    );
}