package com.neighbourmanagement.backend.service;

import com.neighbourmanagement.backend.dto.AutomationCreateRequest;
import com.neighbourmanagement.backend.dto.AutomationResponse;

import java.util.List;

public interface AutomationService {

    AutomationResponse createAutomation(
            AutomationCreateRequest request
    );

    List<AutomationResponse> getAllAutomations();

    AutomationResponse getAutomationById(Long automationId);

    AutomationResponse pauseAutomation(Long automationId);

    AutomationResponse resumeAutomation(Long automationId);

    AutomationResponse endAutomation(Long automationId);

    void deleteAutomation(Long automationId);
}