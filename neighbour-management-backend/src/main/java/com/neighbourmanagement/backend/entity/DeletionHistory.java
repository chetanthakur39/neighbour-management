package com.neighbourmanagement.backend.entity;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "deletion_history")
public class DeletionHistory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "deletion_history_id")
    private Long deletionHistoryId;


    @Column(name = "state", nullable = false)
    private String state;


    @Column(name = "jc", nullable = false)
    private String jc;


    @Column(name = "deleted_count", nullable = false)
    private Integer deletedCount;


    @Column(name = "minimum_neighbours")
    private Integer minimumNeighbours;


    @Column(name = "source", nullable = false)
    private String source;


    @Column(name = "deleted_at", nullable = false)
    private LocalDateTime deletedAt;


    public DeletionHistory() {
    }


    public Long getDeletionHistoryId() {
        return deletionHistoryId;
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


    public Integer getDeletedCount() {
        return deletedCount;
    }


    public void setDeletedCount(
            Integer deletedCount
    ) {
        this.deletedCount = deletedCount;
    }


    public Integer getMinimumNeighbours() {
        return minimumNeighbours;
    }


    public void setMinimumNeighbours(
            Integer minimumNeighbours
    ) {
        this.minimumNeighbours =
                minimumNeighbours;
    }


    public String getSource() {
        return source;
    }


    public void setSource(String source) {
        this.source = source;
    }


    public LocalDateTime getDeletedAt() {
        return deletedAt;
    }


    public void setDeletedAt(
            LocalDateTime deletedAt
    ) {
        this.deletedAt = deletedAt;
    }
}