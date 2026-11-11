package com.neighbourmanagement.backend.repository;

import com.neighbourmanagement.backend.entity.AutomationRule;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

public interface AutomationRuleRepository
        extends JpaRepository<AutomationRule, Long> {

    // =========================================================
    // FIND ALL RULES FOR AUTOMATION
    // =========================================================

    @Query("""
        SELECT r
        FROM AutomationRule r
        WHERE r.automation.automationId = :automationId
    """)
    List<AutomationRule> findRulesByAutomationId(
            @Param("automationId") Long automationId
    );


    // =========================================================
    // FIND ENABLED RULES
    // =========================================================

    List<AutomationRule> findByAutomation_AutomationIdAndEnabledTrue(
            Long automationId
    );


    // =========================================================
    // FIND ALL RULES
    // =========================================================

    List<AutomationRule> findByAutomation_AutomationId(
            Long automationId
    );


    // =========================================================
    // DELETE RULES
    // =========================================================

    @Modifying(
            flushAutomatically = true,
            clearAutomatically = true
    )
    @Transactional
    @Query("""
        DELETE FROM AutomationRule r
        WHERE r.automation.automationId = :automationId
    """)
    void deleteByAutomationId(
            @Param("automationId") Long automationId
    );


    // =========================================================
    // EXISTING COMPATIBILITY METHOD
    // =========================================================

    default void deleteByAutomation_AutomationId(
            Long automationId
    ) {
        deleteByAutomationId(
                automationId
        );
    }
}