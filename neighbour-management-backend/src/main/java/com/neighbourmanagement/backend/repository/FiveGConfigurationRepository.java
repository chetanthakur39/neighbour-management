package com.neighbourmanagement.backend.repository;

import com.neighbourmanagement.backend.entity.FiveGConfiguration;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface FiveGConfigurationRepository
        extends JpaRepository<FiveGConfiguration, Long> {

    Optional<FiveGConfiguration> findByGcellId(Long gcellId);
}