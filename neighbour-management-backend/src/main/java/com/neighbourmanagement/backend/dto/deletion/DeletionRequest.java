package com.neighbourmanagement.backend.dto.deletion;

import java.util.List;

public class DeletionRequest {

    private String state;

    private String jc;

    private Integer minimumNeighbours;

    private List<Long> neighbourIds;

    public DeletionRequest() {
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

    public Integer getMinimumNeighbours() {
        return minimumNeighbours;
    }

    public void setMinimumNeighbours(
            Integer minimumNeighbours
    ) {
        this.minimumNeighbours = minimumNeighbours;
    }

    public List<Long> getNeighbourIds() {
        return neighbourIds;
    }

    public void setNeighbourIds(
            List<Long> neighbourIds
    ) {
        this.neighbourIds = neighbourIds;
    }
}