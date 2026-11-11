package com.neighbourmanagement.backend.controller;

import com.neighbourmanagement.backend.dto.validation.ValidationRequest;
import com.neighbourmanagement.backend.dto.validation.ValidationResponse;
import com.neighbourmanagement.backend.service.ValidationService;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/validation")
@CrossOrigin(origins = "*")
public class ValidationController {

    private final ValidationService validationService;

    public ValidationController(
            ValidationService validationService
    ) {
        this.validationService = validationService;
    }

    @PostMapping("/run")
    public ResponseEntity<ValidationResponse> runValidation(
            @RequestBody ValidationRequest request
    ) {

        ValidationResponse response =
                validationService.runValidation(request);

        return ResponseEntity.ok(response);
    }
}