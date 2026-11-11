package com.neighbourmanagement.backend.controller;

import com.neighbourmanagement.backend.dto.deletion.DeletionRequest;
import com.neighbourmanagement.backend.service.DeletionService;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/deletion")
@CrossOrigin(origins = "*")
public class DeletionController {

    private final DeletionService deletionService;


    public DeletionController(
            DeletionService deletionService
    ) {

        this.deletionService =
                deletionService;
    }


    // =========================================================
    // DIRECT CHATBOT DELETION
    // =========================================================

    @DeleteMapping("/neighbours")
    public ResponseEntity<Map<String, Object>>
    deleteNeighbours(
            @RequestBody DeletionRequest request
    ) {

        int deletedCount =
                deletionService.deleteNeighbours(
                        request
                );


        return ResponseEntity.ok(
                Map.of(
                        "deletedCount",
                        deletedCount,

                        "state",
                        request.getState(),

                        "jc",
                        request.getJc(),

                        "neighbourIds",
                        request.getNeighbourIds()
                )
        );
    }
}