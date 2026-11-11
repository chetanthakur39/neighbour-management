package com.neighbourmanagement.backend.controller;

import com.neighbourmanagement.backend.entity.DeletionHistory;
import com.neighbourmanagement.backend.service.DeletionHistoryService;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/deletion/history")
@CrossOrigin(origins = "*")
public class DeletionHistoryController {

    private final DeletionHistoryService deletionHistoryService;

    public DeletionHistoryController(
            DeletionHistoryService deletionHistoryService
    ) {
        this.deletionHistoryService =
                deletionHistoryService;
    }

    // =========================================================
    // GET ALL DELETION HISTORY
    // =========================================================

    @GetMapping
    public ResponseEntity<List<DeletionHistory>> getAllHistory() {

        return ResponseEntity.ok(
                deletionHistoryService.getAllHistory()
        );
    }

    // =========================================================
    // GET HISTORY FOR SPECIFIC DATE
    // =========================================================

    @GetMapping("/date/{date}")
    public ResponseEntity<List<DeletionHistory>> getHistoryForDate(
            @PathVariable String date
    ) {

        LocalDate localDate =
                LocalDate.parse(date);

        return ResponseEntity.ok(
                deletionHistoryService.getHistoryForDate(
                        localDate
                )
        );
    }

    // =========================================================
    // GET DAILY DELETION TOTAL
    // =========================================================

    @GetMapping("/daily-total")
    public ResponseEntity<Map<String, Object>> getDailyTotal(
            @RequestParam(required = false) String date
    ) {

        LocalDate localDate;

        if (
                date == null
                        || date.isBlank()
        ) {

            localDate = LocalDate.now();

        } else {

            localDate = LocalDate.parse(date);
        }

        Long totalDeleted =
                deletionHistoryService
                        .getTotalDeletedForDate(
                                localDate
                        );

        Map<String, Object> response =
                new LinkedHashMap<>();

        response.put(
                "date",
                localDate.toString()
        );

        response.put(
                "deletedCount",
                totalDeleted
        );

        return ResponseEntity.ok(response);
    }
}
