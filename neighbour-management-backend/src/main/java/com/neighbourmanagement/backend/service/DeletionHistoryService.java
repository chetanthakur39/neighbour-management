package com.neighbourmanagement.backend.service;

import com.neighbourmanagement.backend.entity.DeletionHistory;

import java.time.LocalDate;
import java.util.List;

public interface DeletionHistoryService {

    DeletionHistory recordDeletion(
            String state,
            String jc,
            Integer deletedCount,
            Integer minimumNeighbours,
            String source
    );


    List<DeletionHistory> getAllHistory();


    List<DeletionHistory> getHistoryForDate(
            LocalDate date
    );


    Long getTotalDeletedForDate(
            LocalDate date
    );
}