package com.neighbourmanagement.backend.controller;

import com.neighbourmanagement.backend.dto.AutomationCreateRequest;
import com.neighbourmanagement.backend.dto.AutomationResponse;
import com.neighbourmanagement.backend.service.AutomationService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/automations")
@CrossOrigin(origins = "${APP_CORS_ALLOWED_ORIGINS:http://localhost:5173}")
public class AutomationController {

    private final AutomationService automationService;


    public AutomationController(
            AutomationService automationService
    ) {
        this.automationService = automationService;
    }


    // ==========================================
    // CREATE
    // ==========================================

    @PostMapping
    public ResponseEntity<AutomationResponse>
    createAutomation(
            @RequestBody AutomationCreateRequest request
    ) {

        AutomationResponse response =
                automationService.createAutomation(request);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(response);
    }


    // ==========================================
    // GET ALL
    // ==========================================

    @GetMapping
    public ResponseEntity<List<AutomationResponse>>
    getAllAutomations() {

        return ResponseEntity.ok(
                automationService.getAllAutomations()
        );
    }


    // ==========================================
    // GET BY ID
    // ==========================================

    @GetMapping("/{id}")
    public ResponseEntity<AutomationResponse>
    getAutomation(
            @PathVariable Long id
    ) {

        return ResponseEntity.ok(
                automationService.getAutomationById(id)
        );
    }


    // ==========================================
    // PAUSE
    // ==========================================

    @PutMapping("/{id}/pause")
    public ResponseEntity<AutomationResponse>
    pauseAutomation(
            @PathVariable Long id
    ) {

        return ResponseEntity.ok(
                automationService.pauseAutomation(id)
        );
    }


    // ==========================================
    // RESUME
    // ==========================================

    @PutMapping("/{id}/resume")
    public ResponseEntity<AutomationResponse>
    resumeAutomation(
            @PathVariable Long id
    ) {

        return ResponseEntity.ok(
                automationService.resumeAutomation(id)
        );
    }


    // ==========================================
    // END
    // ==========================================

    @PutMapping("/{id}/end")
    public ResponseEntity<AutomationResponse>
    endAutomation(
            @PathVariable Long id
    ) {

        return ResponseEntity.ok(
                automationService.endAutomation(id)
        );
    }


    // ==========================================
    // DELETE
    // ==========================================

    @DeleteMapping("/{id}")
    public ResponseEntity<Void>
    deleteAutomation(
            @PathVariable Long id
    ) {

        automationService.deleteAutomation(id);

        return ResponseEntity.noContent().build();
    }
}
