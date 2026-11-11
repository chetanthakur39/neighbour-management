package com.neighbourmanagement.backend.dto.validation;

import java.util.List;

public class ValidationResponse {

    private String state;

    private String jc;

    private Integer totalNeighbours;

    private Integer validNeighbours;

    private Integer invalidNeighbours;

    private List<ValidationResultResponse> results;

    public ValidationResponse() {
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

    public Integer getTotalNeighbours() {
        return totalNeighbours;
    }

    public void setTotalNeighbours(Integer totalNeighbours) {
        this.totalNeighbours = totalNeighbours;
    }

    public Integer getValidNeighbours() {
        return validNeighbours;
    }

    public void setValidNeighbours(Integer validNeighbours) {
        this.validNeighbours = validNeighbours;
    }

    public Integer getInvalidNeighbours() {
        return invalidNeighbours;
    }

    public void setInvalidNeighbours(Integer invalidNeighbours) {
        this.invalidNeighbours = invalidNeighbours;
    }

    public List<ValidationResultResponse> getResults() {
        return results;
    }

    public void setResults(List<ValidationResultResponse> results) {
        this.results = results;
    }
}