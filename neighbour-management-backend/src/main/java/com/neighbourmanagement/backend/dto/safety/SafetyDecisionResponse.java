package com.neighbourmanagement.backend.dto.safety;

import java.util.List;

public class SafetyDecisionResponse {

    private Integer totalNeighbours;

    private Integer validNeighbours;

    private Integer invalidNeighbours;

    private Integer minimumNeighbours;

    private Integer neighboursToDelete;

    private Integer neighboursToRetain;

    private boolean deletionAllowed;

    private List<Long> neighbourIdsToDelete;

    private List<Long> neighbourIdsToRetain;

    public SafetyDecisionResponse() {
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

    public Integer getMinimumNeighbours() {
        return minimumNeighbours;
    }

    public void setMinimumNeighbours(Integer minimumNeighbours) {
        this.minimumNeighbours = minimumNeighbours;
    }

    public Integer getNeighboursToDelete() {
        return neighboursToDelete;
    }

    public void setNeighboursToDelete(Integer neighboursToDelete) {
        this.neighboursToDelete = neighboursToDelete;
    }

    public Integer getNeighboursToRetain() {
        return neighboursToRetain;
    }

    public void setNeighboursToRetain(Integer neighboursToRetain) {
        this.neighboursToRetain = neighboursToRetain;
    }

    public boolean isDeletionAllowed() {
        return deletionAllowed;
    }

    public void setDeletionAllowed(boolean deletionAllowed) {
        this.deletionAllowed = deletionAllowed;
    }

    public List<Long> getNeighbourIdsToDelete() {
        return neighbourIdsToDelete;
    }

    public void setNeighbourIdsToDelete(
            List<Long> neighbourIdsToDelete
    ) {
        this.neighbourIdsToDelete =
                neighbourIdsToDelete;
    }

    public List<Long> getNeighbourIdsToRetain() {
        return neighbourIdsToRetain;
    }

    public void setNeighbourIdsToRetain(
            List<Long> neighbourIdsToRetain
    ) {
        this.neighbourIdsToRetain =
                neighbourIdsToRetain;
    }
}