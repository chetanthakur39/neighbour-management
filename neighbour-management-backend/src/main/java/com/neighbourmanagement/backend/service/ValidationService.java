package com.neighbourmanagement.backend.service;

import com.neighbourmanagement.backend.dto.validation.ValidationRequest;
import com.neighbourmanagement.backend.dto.validation.ValidationResponse;

public interface ValidationService {

    ValidationResponse runValidation(
            ValidationRequest request
    );
}