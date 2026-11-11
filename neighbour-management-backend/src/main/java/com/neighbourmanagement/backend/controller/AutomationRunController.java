package com.neighbourmanagement.backend.controller;

import com.neighbourmanagement.backend.service.AutomationRunService;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/automations")
@CrossOrigin(origins = "*")
public class AutomationRunController {

    private final AutomationRunService automationRunService;

    public AutomationRunController(
            AutomationRunService automationRunService
    ) {
        this.automationRunService =
                automationRunService;
    }

    @PostMapping("/{automationId}/run")
    public ResponseEntity<Object> runAutomation(
            @PathVariable Long automationId
    ) {

        Object response =
                automationRunService.runAutomation(
                        automationId
                );

        return ResponseEntity.ok(response);
    }
}