package com.neighbourmanagement.backend.dto;

import com.neighbourmanagement.backend.enums.AutomationRuleType;
import com.neighbourmanagement.backend.enums.AutomationStatus;
import com.neighbourmanagement.backend.enums.TechnologyFlow;

import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;

public class AutomationResponse {

    private Long automationId;

    private String name;

    private String state;

    private String jc;

    private TechnologyFlow technologyFlow;

    private String frequency;

    private LocalTime executionTime;

    private Integer minimumNeighbours;

    private AutomationStatus status;

    private LocalDateTime lastRunAt;

    private LocalDateTime nextRunAt;

    private LocalDateTime createdAt;

    private List<AutomationRuleType> rules;


    public AutomationResponse() {
    }


    public Long getAutomationId() {
        return automationId;
    }

    public void setAutomationId(Long automationId) {
        this.automationId = automationId;
    }


    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }


    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }


    public String getJc() {
        return jc;
    }

    public void setJc(String jc) {
        this.jc = jc;
    }


    public TechnologyFlow getTechnologyFlow() {
        return technologyFlow;
    }

    public void setTechnologyFlow(TechnologyFlow technologyFlow) {
        this.technologyFlow = technologyFlow;
    }


    public String getFrequency() {
        return frequency;
    }

    public void setFrequency(String frequency) {
        this.frequency = frequency;
    }


    public LocalTime getExecutionTime() {
        return executionTime;
    }

    public void setExecutionTime(LocalTime executionTime) {
        this.executionTime = executionTime;
    }


    public Integer getMinimumNeighbours() {
        return minimumNeighbours;
    }

    public void setMinimumNeighbours(Integer minimumNeighbours) {
        this.minimumNeighbours = minimumNeighbours;
    }


    public AutomationStatus getStatus() {
        return status;
    }

    public void setStatus(AutomationStatus status) {
        this.status = status;
    }


    public LocalDateTime getLastRunAt() {
        return lastRunAt;
    }

    public void setLastRunAt(LocalDateTime lastRunAt) {
        this.lastRunAt = lastRunAt;
    }


    public LocalDateTime getNextRunAt() {
        return nextRunAt;
    }

    public void setNextRunAt(LocalDateTime nextRunAt) {
        this.nextRunAt = nextRunAt;
    }


    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }


    public List<AutomationRuleType> getRules() {
        return rules;
    }

    public void setRules(List<AutomationRuleType> rules) {
        this.rules = rules;
    }
}