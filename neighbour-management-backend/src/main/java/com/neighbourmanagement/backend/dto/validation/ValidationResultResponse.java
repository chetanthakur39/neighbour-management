package com.neighbourmanagement.backend.dto.validation;

import java.util.List;

public class ValidationResultResponse {

    private Long neighbourId;

    private String sourceCell;

    private String targetCell;

    private Integer sourcePci;

    private Integer targetPci;

    private Integer sourceTac;

    private Integer targetTac;

    private String status;

    private List<String> failedRules;

    public ValidationResultResponse() {
    }

    public Long getNeighbourId() {
        return neighbourId;
    }

    public void setNeighbourId(Long neighbourId) {
        this.neighbourId = neighbourId;
    }

    public String getSourceCell() {
        return sourceCell;
    }

    public void setSourceCell(String sourceCell) {
        this.sourceCell = sourceCell;
    }

    public String getTargetCell() {
        return targetCell;
    }

    public void setTargetCell(String targetCell) {
        this.targetCell = targetCell;
    }

    public Integer getSourcePci() {
        return sourcePci;
    }

    public void setSourcePci(Integer sourcePci) {
        this.sourcePci = sourcePci;
    }

    public Integer getTargetPci() {
        return targetPci;
    }

    public void setTargetPci(Integer targetPci) {
        this.targetPci = targetPci;
    }

    public Integer getSourceTac() {
        return sourceTac;
    }

    public void setSourceTac(Integer sourceTac) {
        this.sourceTac = sourceTac;
    }

    public Integer getTargetTac() {
        return targetTac;
    }

    public void setTargetTac(Integer targetTac) {
        this.targetTac = targetTac;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public List<String> getFailedRules() {
        return failedRules;
    }

    public void setFailedRules(List<String> failedRules) {
        this.failedRules = failedRules;
    }
}