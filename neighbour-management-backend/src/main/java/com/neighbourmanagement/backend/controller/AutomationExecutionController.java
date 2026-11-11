package com.neighbourmanagement.backend.controller;

import com.neighbourmanagement.backend.entity.AutomationExecution;
import com.neighbourmanagement.backend.service.AutomationExecutionService;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/automation-executions")
@CrossOrigin(origins = "*")
public class AutomationExecutionController {

    private final AutomationExecutionService automationExecutionService;

    public AutomationExecutionController(
            AutomationExecutionService automationExecutionService
    ) {
        this.automationExecutionService =
                automationExecutionService;
    }

    @GetMapping("/automation/{automationId}")
    public ResponseEntity<List<AutomationExecution>> getExecutions(
            @PathVariable Long automationId
    ) {

        return ResponseEntity.ok(
                automationExecutionService.getExecutions(
                        automationId
                )
        );
    }
}