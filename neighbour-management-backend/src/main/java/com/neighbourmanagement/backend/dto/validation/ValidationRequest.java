package com.neighbourmanagement.backend.dto.validation;

import com.neighbourmanagement.backend.enums.AutomationRuleType;

import java.util.List;

public class ValidationRequest {

    private String state;

    private String jc;

    private List<AutomationRuleType> rules;

    public ValidationRequest() {
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

    public List<AutomationRuleType> getRules() {
        return rules;
    }

    public void setRules(List<AutomationRuleType> rules) {
        this.rules = rules;
    }
}