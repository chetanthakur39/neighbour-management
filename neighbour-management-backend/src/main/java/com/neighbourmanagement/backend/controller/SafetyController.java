package com.neighbourmanagement.backend.controller;

import com.neighbourmanagement.backend.dto.safety.SafetyDecisionResponse;
import com.neighbourmanagement.backend.dto.validation.ValidationResponse;
import com.neighbourmanagement.backend.service.SafetyService;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/safety")
@CrossOrigin(origins = "*")
public class SafetyController {

    private final SafetyService safetyService;

    public SafetyController(
            SafetyService safetyService
    ) {
        this.safetyService = safetyService;
    }

    @PostMapping("/evaluate")
    public ResponseEntity<SafetyDecisionResponse> evaluate(
            @RequestBody ValidationResponse validationResponse,
            @RequestParam(defaultValue = "5")
            Integer minimumNeighbours
    ) {

        SafetyDecisionResponse response =
                safetyService.evaluate(
                        validationResponse,
                        minimumNeighbours
                );

        return ResponseEntity.ok(response);
    }
}