package com.neighbourmanagement.backend.controller;

import com.neighbourmanagement.backend.repository.MetadataRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/metadata")
@CrossOrigin(origins = "*")
public class MetadataController {

    private final MetadataRepository metadataRepository;

    public MetadataController(
            MetadataRepository metadataRepository
    ) {
        this.metadataRepository = metadataRepository;
    }

    // ========================================================
    // GET ALL STATES
    // ========================================================

    @GetMapping("/states")
    public ResponseEntity<List<String>> getStates() {

        return ResponseEntity.ok(
                metadataRepository.findAllStates()
        );
    }

    // ========================================================
    // GET ALL JCs
    // ========================================================

    @GetMapping("/jcs")
    public ResponseEntity<List<String>> getAllJcs() {

        return ResponseEntity.ok(
                metadataRepository.findAllJcs()
        );
    }

    // ========================================================
    // GET JCs FOR A STATE
    // ========================================================

    @GetMapping("/jcs/{state}")
    public ResponseEntity<List<String>> getJcsByState(
            @PathVariable String state
    ) {

        return ResponseEntity.ok(
                metadataRepository.findJcsByState(
                        state
                )
        );
    }

    // ========================================================
    // CHECK STATE + JC
    // ========================================================

    @GetMapping("/state-jc/exists")
    public ResponseEntity<Map<String, Object>> checkStateJc(
            @RequestParam String state,
            @RequestParam String jc
    ) {

        long count =
                metadataRepository.countStateJc(
                        state,
                        jc
                );

        return ResponseEntity.ok(
                Map.of(
                        "state", state,
                        "jc", jc,
                        "exists", count > 0
                )
        );
    }
}