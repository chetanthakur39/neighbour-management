package com.neighbourmanagement.backend.controller;

import com.neighbourmanagement.backend.dto.safety.SafetyDecisionResponse;
import com.neighbourmanagement.backend.dto.validation.ValidationRequest;
import com.neighbourmanagement.backend.dto.validation.ValidationResponse;
import com.neighbourmanagement.backend.service.SafetyService;
import com.neighbourmanagement.backend.service.ValidationService;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/validation")
@CrossOrigin(origins = "*")
public class ValidationPreviewController {

    private final ValidationService validationService;

    private final SafetyService safetyService;


    public ValidationPreviewController(
            ValidationService validationService,
            SafetyService safetyService
    ) {

        this.validationService =
                validationService;

        this.safetyService =
                safetyService;
    }


    @PostMapping("/preview")
    public ResponseEntity<SafetyDecisionResponse> previewValidation(
            @RequestParam Integer minimumNeighbours,
            @RequestBody ValidationRequest request
    ) {

        // =====================================================
        // 1. RUN VALIDATION
        // =====================================================

        ValidationResponse validationResponse =
                validationService.runValidation(
                        request
                );


        // =====================================================
        // 2. RUN SAFETY
        // =====================================================

        SafetyDecisionResponse safetyResponse =
                safetyService.evaluate(
                        validationResponse,
                        minimumNeighbours
                );


        // =====================================================
        // 3. RETURN SAFETY RESULT
        // =====================================================

        return ResponseEntity.ok(
                safetyResponse
        );
    }
}