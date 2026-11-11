package com.neighbourmanagement.backend.entity;

import jakarta.persistence.*;

import java.math.BigDecimal;

@Entity
@Table(name = "4g_configuration")
public class FourGConfiguration {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "config_id")
    private Long configId;

    @Column(name = "ecell_id", nullable = false, unique = true)
    private Long ecellId;

    @Column(name = "bandwidth_mhz", nullable = false)
    private Integer bandwidthMhz;

    @Column(name = "tx_power_dbm")
    private BigDecimal txPowerDbm;

    @Column(name = "antenna_configuration")
    private String antennaConfiguration;

    @Column(name = "handover_enabled")
    private Boolean handoverEnabled;

    @Column(name = "rsrp_threshold_dbm")
    private BigDecimal rsrpThresholdDbm;

    @Column(name = "rsrq_threshold_db")
    private BigDecimal rsrqThresholdDb;

    @Column(name = "configuration_status")
    private String configurationStatus;

    @Column(name = "source")
    private String source;

    @Column(name = "Technology")
    private String technology;

    @Column(name = "PCI")
    private Integer pci;

    @Column(name = "TAC")
    private Integer tac;

    public FourGConfiguration() {
    }

    public Long getConfigId() {
        return configId;
    }

    public Long getEcellId() {
        return ecellId;
    }

    public void setEcellId(Long ecellId) {
        this.ecellId = ecellId;
    }

    public Integer getPci() {
        return pci;
    }

    public void setPci(Integer pci) {
        this.pci = pci;
    }

    public Integer getTac() {
        return tac;
    }

    public void setTac(Integer tac) {
        this.tac = tac;
    }

    public Integer getBandwidthMhz() {
        return bandwidthMhz;
    }

    public void setBandwidthMhz(Integer bandwidthMhz) {
        this.bandwidthMhz = bandwidthMhz;
    }

    public BigDecimal getTxPowerDbm() {
        return txPowerDbm;
    }

    public void setTxPowerDbm(BigDecimal txPowerDbm) {
        this.txPowerDbm = txPowerDbm;
    }

    public String getAntennaConfiguration() {
        return antennaConfiguration;
    }

    public void setAntennaConfiguration(String antennaConfiguration) {
        this.antennaConfiguration = antennaConfiguration;
    }

    public Boolean getHandoverEnabled() {
        return handoverEnabled;
    }

    public void setHandoverEnabled(Boolean handoverEnabled) {
        this.handoverEnabled = handoverEnabled;
    }

    public BigDecimal getRsrpThresholdDbm() {
        return rsrpThresholdDbm;
    }

    public void setRsrpThresholdDbm(BigDecimal rsrpThresholdDbm) {
        this.rsrpThresholdDbm = rsrpThresholdDbm;
    }

    public String getConfigurationStatus() {
        return configurationStatus;
    }

    public void setConfigurationStatus(String configurationStatus) {
        this.configurationStatus = configurationStatus;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getTechnology() {
        return technology;
    }

    public void setTechnology(String technology) {
        this.technology = technology;
    }
}