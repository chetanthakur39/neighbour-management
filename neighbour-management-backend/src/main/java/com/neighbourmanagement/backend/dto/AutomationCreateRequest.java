package com.neighbourmanagement.backend.dto;

import com.neighbourmanagement.backend.enums.AutomationRuleType;
import com.neighbourmanagement.backend.enums.TechnologyFlow;

import java.time.LocalTime;
import java.util.List;

public class AutomationCreateRequest {

    private String name;

    private String state;

    private String jc;

    private TechnologyFlow technologyFlow;

    private LocalTime executionTime;

    private Integer minimumNeighbours;

    private List<AutomationRuleType> rules;


    public AutomationCreateRequest() {
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


    public List<AutomationRuleType> getRules() {
        return rules;
    }

    public void setRules(List<AutomationRuleType> rules) {
        this.rules = rules;
    }
}