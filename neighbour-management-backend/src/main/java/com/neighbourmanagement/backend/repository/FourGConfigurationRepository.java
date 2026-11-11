package com.neighbourmanagement.backend.repository;

import com.neighbourmanagement.backend.entity.FourGConfiguration;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface FourGConfigurationRepository
        extends JpaRepository<FourGConfiguration, Long> {

    Optional<FourGConfiguration> findByEcellId(Long ecellId);
}