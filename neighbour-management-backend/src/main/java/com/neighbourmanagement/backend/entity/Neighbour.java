package com.neighbourmanagement.backend.entity;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "neighbour")
public class Neighbour {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "neighbour_id")
    private Long neighbourId;


    // ==========================================
    // NETWORK REFERENCES
    // ==========================================

    @Column(name = "ecell_id", nullable = false)
    private Long ecellId;

    @Column(name = "gcell_id", nullable = false)
    private Long gcellId;


    // ==========================================
    // NEIGHBOUR INFORMATION
    // ==========================================

    @Column(name = "handover_count")
    private Long handoverCount;

    @Column(
            name = "distance_km",
            precision = 10,
            scale = 3,
            nullable = false
    )
    private BigDecimal distanceKm;

    @Column(name = "relation_index", nullable = false)
    private Integer relationIndex;

    @Column(name = "status", length = 20)
    private String status;


    // ==========================================
    // AUDIT
    // ==========================================

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;


    // ==========================================
    // SOURCE
    // ==========================================

    @Column(name = "source")
    private String source;

    @Column(name = "source_cell", nullable = false)
    private String sourceCell;

    @Column(name = "source_pci")
    private Integer sourcePci;

    @Column(name = "source_tac")
    private Integer sourceTac;

    @Column(name = "source_technology")
    private String sourceTechnology;


    // ==========================================
    // TARGET
    // ==========================================

    @Column(name = "target_cell", nullable = false)
    private String targetCell;

    @Column(name = "target_pci")
    private Integer targetPci;

    @Column(name = "target_tac")
    private Integer targetTac;

    @Column(name = "target_technology")
    private String targetTechnology;


    // ==========================================
    // CONSTRUCTOR
    // ==========================================

    public Neighbour() {
    }


    // ==========================================
    // GETTERS
    // ==========================================

    public Long getNeighbourId() {
        return neighbourId;
    }

    public Long getEcellId() {
        return ecellId;
    }

    public Long getGcellId() {
        return gcellId;
    }

    public Long getHandoverCount() {
        return handoverCount;
    }

    public BigDecimal getDistanceKm() {
        return distanceKm;
    }

    public Integer getRelationIndex() {
        return relationIndex;
    }

    public String getStatus() {
        return status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public String getSource() {
        return source;
    }

    public String getSourceCell() {
        return sourceCell;
    }

    public Integer getSourcePci() {
        return sourcePci;
    }

    public Integer getSourceTac() {
        return sourceTac;
    }

    public String getSourceTechnology() {
        return sourceTechnology;
    }

    public String getTargetCell() {
        return targetCell;
    }

    public Integer getTargetPci() {
        return targetPci;
    }

    public Integer getTargetTac() {
        return targetTac;
    }

    public String getTargetTechnology() {
        return targetTechnology;
    }


    // ==========================================
    // SETTERS
    // ==========================================

    public void setEcellId(Long ecellId) {
        this.ecellId = ecellId;
    }

    public void setGcellId(Long gcellId) {
        this.gcellId = gcellId;
    }

    public void setHandoverCount(Long handoverCount) {
        this.handoverCount = handoverCount;
    }

    public void setDistanceKm(BigDecimal distanceKm) {
        this.distanceKm = distanceKm;
    }

    public void setRelationIndex(Integer relationIndex) {
        this.relationIndex = relationIndex;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public void setSourceCell(String sourceCell) {
        this.sourceCell = sourceCell;
    }

    public void setSourcePci(Integer sourcePci) {
        this.sourcePci = sourcePci;
    }

    public void setSourceTac(Integer sourceTac) {
        this.sourceTac = sourceTac;
    }

    public void setSourceTechnology(String sourceTechnology) {
        this.sourceTechnology = sourceTechnology;
    }

    public void setTargetCell(String targetCell) {
        this.targetCell = targetCell;
    }

    public void setTargetPci(Integer targetPci) {
        this.targetPci = targetPci;
    }

    public void setTargetTac(Integer targetTac) {
        this.targetTac = targetTac;
    }

    public void setTargetTechnology(String targetTechnology) {
        this.targetTechnology = targetTechnology;
    }
}