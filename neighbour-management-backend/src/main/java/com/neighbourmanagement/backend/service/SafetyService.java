package com.neighbourmanagement.backend.service;

import com.neighbourmanagement.backend.dto.safety.SafetyDecisionResponse;
import com.neighbourmanagement.backend.dto.validation.ValidationResponse;

public interface SafetyService {

    SafetyDecisionResponse evaluate(
            ValidationResponse validationResponse,
            Integer minimumNeighbours
    );
}