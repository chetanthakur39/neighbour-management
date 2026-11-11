package com.neighbourmanagement.backend.entity;

import com.neighbourmanagement.backend.enums.AutomationStatus;
import com.neighbourmanagement.backend.enums.TechnologyFlow;
import jakarta.persistence.*;

import java.time.LocalDateTime;
import java.time.LocalTime;

@Entity
@Table(name = "automation")
public class Automation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "automation_id")
    private Long automationId;


    // Automation name
    @Column(name = "name", nullable = false, length = 100)
    private String name;


    // Selected State
    @Column(name = "state", nullable = false, length = 100)
    private String state;


    // Selected JC
    @Column(name = "jc", nullable = false, length = 100)
    private String jc;


    // 4G -> 5G / 5G -> 4G
    @Enumerated(EnumType.STRING)
    @Column(
            name = "technology_flow",
            nullable = false,
            length = 30
    )
    private TechnologyFlow technologyFlow;


    // Currently only DAILY
    @Column(name = "frequency", nullable = false, length = 20)
    private String frequency = "DAILY";


    // Example: 10:30
    @Column(name = "execution_time", nullable = false)
    private LocalTime executionTime;


    // Minimum neighbours to retain
    @Column(name = "minimum_neighbours", nullable = false)
    private Integer minimumNeighbours = 5;


    // RUNNING / PAUSED / ENDED
    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 20)
    private AutomationStatus status = AutomationStatus.RUNNING;


    // Last execution
    @Column(name = "last_run_at")
    private LocalDateTime lastRunAt;


    // Next scheduled execution
    @Column(name = "next_run_at")
    private LocalDateTime nextRunAt;


    // Created
    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;


    // Updated
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;


    // Automation started
    @Column(name = "started_at")
    private LocalDateTime startedAt;


    // Automation paused
    @Column(name = "paused_at")
    private LocalDateTime pausedAt;


    // Automation ended
    @Column(name = "ended_at")
    private LocalDateTime endedAt;


    // ==========================================
    // CONSTRUCTOR
    // ==========================================

    public Automation() {
    }


    // ==========================================
    // JPA CALLBACKS
    // ==========================================

    @PrePersist
    protected void onCreate() {

        LocalDateTime now = LocalDateTime.now();

        createdAt = now;
        updatedAt = now;

        if (startedAt == null) {
            startedAt = now;
        }
    }


    @PreUpdate
    protected void onUpdate() {

        updatedAt = LocalDateTime.now();
    }


    // ==========================================
    // GETTERS
    // ==========================================

    public Long getAutomationId() {
        return automationId;
    }

    public String getName() {
        return name;
    }

    public String getState() {
        return state;
    }

    public String getJc() {
        return jc;
    }

    public TechnologyFlow getTechnologyFlow() {
        return technologyFlow;
    }

    public String getFrequency() {
        return frequency;
    }

    public LocalTime getExecutionTime() {
        return executionTime;
    }

    public Integer getMinimumNeighbours() {
        return minimumNeighbours;
    }

    public AutomationStatus getStatus() {
        return status;
    }

    public LocalDateTime getLastRunAt() {
        return lastRunAt;
    }

    public LocalDateTime getNextRunAt() {
        return nextRunAt;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public LocalDateTime getStartedAt() {
        return startedAt;
    }

    public LocalDateTime getPausedAt() {
        return pausedAt;
    }

    public LocalDateTime getEndedAt() {
        return endedAt;
    }


    // ==========================================
    // SETTERS
    // ==========================================

    public void setName(String name) {
        this.name = name;
    }

    public void setState(String state) {
        this.state = state;
    }

    public void setJc(String jc) {
        this.jc = jc;
    }

    public void setTechnologyFlow(TechnologyFlow technologyFlow) {
        this.technologyFlow = technologyFlow;
    }

    public void setFrequency(String frequency) {
        this.frequency = frequency;
    }

    public void setExecutionTime(LocalTime executionTime) {
        this.executionTime = executionTime;
    }

    public void setMinimumNeighbours(Integer minimumNeighbours) {
        this.minimumNeighbours = minimumNeighbours;
    }

    public void setStatus(AutomationStatus status) {
        this.status = status;
    }

    public void setLastRunAt(LocalDateTime lastRunAt) {
        this.lastRunAt = lastRunAt;
    }

    public void setNextRunAt(LocalDateTime nextRunAt) {
        this.nextRunAt = nextRunAt;
    }

    public void setStartedAt(LocalDateTime startedAt) {
        this.startedAt = startedAt;
    }

    public void setPausedAt(LocalDateTime pausedAt) {
        this.pausedAt = pausedAt;
    }

    public void setEndedAt(LocalDateTime endedAt) {
        this.endedAt = endedAt;
    }
}