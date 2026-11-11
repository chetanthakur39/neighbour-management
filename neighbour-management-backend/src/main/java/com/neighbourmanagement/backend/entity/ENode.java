package com.neighbourmanagement.backend.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "enodes")
public class ENode {

    @Id
    @Column(name = "enode_id")
    private Long enodeId;

    @Column(name = "enode_name")
    private String enodeName;

    @Column(name = "site_name")
    private String siteName;

    @Column(name = "latitude")
    private Double latitude;

    @Column(name = "longitude")
    private Double longitude;

    @Column(name = "location")
    private String location;

    @Column(name = "status")
    private String status;

    @Column(name = "vendor")
    private String vendor;

    @Column(name = "state")
    private String state;

    @Column(name = "jc")
    private String jc;

    public ENode() {
    }

    public Long getEnodeId() {
        return enodeId;
    }

    public void setEnodeId(Long enodeId) {
        this.enodeId = enodeId;
    }

    public String getEnodeName() {
        return enodeName;
    }

    public void setEnodeName(String enodeName) {
        this.enodeName = enodeName;
    }

    public String getSiteName() {
        return siteName;
    }

    public void setSiteName(String siteName) {
        this.siteName = siteName;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getVendor() {
        return vendor;
    }

    public void setVendor(String vendor) {
        this.vendor = vendor;
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
}