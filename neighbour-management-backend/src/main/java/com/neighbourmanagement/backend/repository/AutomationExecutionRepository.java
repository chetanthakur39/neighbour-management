package com.neighbourmanagement.backend.repository;

import com.neighbourmanagement.backend.entity.AutomationExecution;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDateTime;
import java.util.List;

public interface AutomationExecutionRepository
        extends JpaRepository<AutomationExecution, Long> {

    List<AutomationExecution>
    findByAutomation_AutomationIdOrderByStartedAtDesc(
            Long automationId
    );

    List<AutomationExecution>
    findByStartedAtBetweenOrderByStartedAtDesc(
            LocalDateTime start,
            LocalDateTime end
    );

    void deleteByAutomation_AutomationId(
            Long automationId
    );
}