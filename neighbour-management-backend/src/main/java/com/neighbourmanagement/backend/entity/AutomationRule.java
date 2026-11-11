package com.neighbourmanagement.backend.entity;

import com.neighbourmanagement.backend.enums.AutomationRuleType;
import jakarta.persistence.*;

@Entity
@Table(
        name = "automation_rule",
        uniqueConstraints = {
                @UniqueConstraint(
                        name = "uk_automation_rule",
                        columnNames = {
                                "automation_id",
                                "rule_type"
                        }
                )
        }
)
public class AutomationRule {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "rule_id")
    private Long ruleId;


    // Automation to which this rule belongs
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(
            name = "automation_id",
            nullable = false
    )
    private Automation automation;


    // PCI / TAC / SOURCE / TECHNOLOGY
    @Enumerated(EnumType.STRING)
    @Column(
            name = "rule_type",
            nullable = false,
            length = 20
    )
    private AutomationRuleType ruleType;


    // Is this rule enabled?
    @Column(name = "enabled", nullable = false)
    private boolean enabled = true;


    // ==========================================
    // CONSTRUCTOR
    // ==========================================

    public AutomationRule() {
    }


    // ==========================================
    // GETTERS
    // ==========================================

    public Long getRuleId() {
        return ruleId;
    }

    public Automation getAutomation() {
        return automation;
    }

    public AutomationRuleType getRuleType() {
        return ruleType;
    }

    public boolean isEnabled() {
        return enabled;
    }


    // ==========================================
    // SETTERS
    // ==========================================

    public void setAutomation(Automation automation) {
        this.automation = automation;
    }

    public void setRuleType(AutomationRuleType ruleType) {
        this.ruleType = ruleType;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }
}
