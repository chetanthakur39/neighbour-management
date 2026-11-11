package com.neighbourmanagement.backend.entity;

import com.neighbourmanagement.backend.enums.ExecutionStatus;
import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "automation_execution")
public class AutomationExecution {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "execution_id")
    private Long executionId;


    // =========================================================
    // AUTOMATION
    // =========================================================

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(
            name = "automation_id",
            nullable = false
    )
    private Automation automation;


    // =========================================================
    // EXECUTION INFORMATION
    // =========================================================

    @Column(name = "started_at", nullable = false)
    private LocalDateTime startedAt;

    @Column(name = "completed_at")
    private LocalDateTime completedAt;


    // =========================================================
    // LOCATION
    // =========================================================

    @Column(name = "state", nullable = false)
    private String state;

    @Column(name = "jc", nullable = false)
    private String jc;


    // =========================================================
    // COUNTS
    // =========================================================

    @Column(name = "total_checked", nullable = false)
    private Integer totalChecked;

    @Column(name = "valid_count", nullable = false)
    private Integer validCount;

    @Column(name = "invalid_count", nullable = false)
    private Integer invalidCount;

    @Column(name = "deleted_count", nullable = false)
    private Integer deletedCount;

    @Column(name = "retained_count", nullable = false)
    private Integer retainedCount;


    // =========================================================
    // STATUS
    // =========================================================

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private ExecutionStatus status;


    // =========================================================
    // ERROR
    // =========================================================

    @Column(name = "error_message", columnDefinition = "TEXT")
    private String errorMessage;


    // =========================================================
    // CONSTRUCTOR
    // =========================================================

    public AutomationExecution() {
    }


    // =========================================================
    // GETTERS
    // =========================================================

    public Long getExecutionId() {
        return executionId;
    }

    public Automation getAutomation() {
        return automation;
    }

    public LocalDateTime getStartedAt() {
        return startedAt;
    }

    public LocalDateTime getCompletedAt() {
        return completedAt;
    }

    public String getState() {
        return state;
    }

    public String getJc() {
        return jc;
    }

    public Integer getTotalChecked() {
        return totalChecked;
    }

    public Integer getValidCount() {
        return validCount;
    }

    public Integer getInvalidCount() {
        return invalidCount;
    }

    public Integer getDeletedCount() {
        return deletedCount;
    }

    public Integer getRetainedCount() {
        return retainedCount;
    }

    public ExecutionStatus getStatus() {
        return status;
    }

    public String getErrorMessage() {
        return errorMessage;
    }


    // =========================================================
    // SETTERS
    // =========================================================

    public void setAutomation(
            Automation automation
    ) {
        this.automation = automation;
    }

    public void setStartedAt(
            LocalDateTime startedAt
    ) {
        this.startedAt = startedAt;
    }

    public void setCompletedAt(
            LocalDateTime completedAt
    ) {
        this.completedAt = completedAt;
    }

    public void setState(
            String state
    ) {
        this.state = state;
    }

    public void setJc(
            String jc
    ) {
        this.jc = jc;
    }

    public void setTotalChecked(
            Integer totalChecked
    ) {
        this.totalChecked = totalChecked;
    }

    public void setValidCount(
            Integer validCount
    ) {
        this.validCount = validCount;
    }

    public void setInvalidCount(
            Integer invalidCount
    ) {
        this.invalidCount = invalidCount;
    }

    public void setDeletedCount(
            Integer deletedCount
    ) {
        this.deletedCount = deletedCount;
    }

    public void setRetainedCount(
            Integer retainedCount
    ) {
        this.retainedCount = retainedCount;
    }

    public void setStatus(
            ExecutionStatus status
    ) {
        this.status = status;
    }

    public void setErrorMessage(
            String errorMessage
    ) {
        this.errorMessage = errorMessage;
    }
}