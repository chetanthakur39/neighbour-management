package com.neighbourmanagement.backend.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "ecell")
public class ECell {

    @Id
    @Column(name = "ecell_id")
    private Long ecellId;

    @Column(name = "enode_id", nullable = false)
    private Long enodeId;

    @Column(name = "cell_name")
    private String cellName;

    @Column(name = "cell_index")
    private Integer cellIndex;

    @Column(name = "band")
    private String band;

    @Column(name = "frequency")
    private Integer frequency;

    @Column(name = "azimuth")
    private Double azimuth;

    @Column(name = "status")
    private String status;

    public ECell() {
    }

    public Long getEcellId() {
        return ecellId;
    }

    public void setEcellId(Long ecellId) {
        this.ecellId = ecellId;
    }

    public Long getEnodeId() {
        return enodeId;
    }

    public void setEnodeId(Long enodeId) {
        this.enodeId = enodeId;
    }

    public String getCellName() {
        return cellName;
    }

    public void setCellName(String cellName) {
        this.cellName = cellName;
    }

    public Integer getCellIndex() {
        return cellIndex;
    }

    public void setCellIndex(Integer cellIndex) {
        this.cellIndex = cellIndex;
    }

    public String getBand() {
        return band;
    }

    public void setBand(String band) {
        this.band = band;
    }

    public Integer getFrequency() {
        return frequency;
    }

    public void setFrequency(Integer frequency) {
        this.frequency = frequency;
    }

    public Double getAzimuth() {
        return azimuth;
    }

    public void setAzimuth(Double azimuth) {
        this.azimuth = azimuth;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}