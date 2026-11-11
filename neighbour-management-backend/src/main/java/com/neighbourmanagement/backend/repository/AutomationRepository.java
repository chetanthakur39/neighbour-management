package com.neighbourmanagement.backend.repository;

import com.neighbourmanagement.backend.entity.Automation;
import com.neighbourmanagement.backend.enums.AutomationStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AutomationRepository
        extends JpaRepository<Automation, Long> {

    List<Automation> findByStatus(
            AutomationStatus status
    );

    List<Automation> findByStateAndJc(
            String state,
            String jc
    );
}