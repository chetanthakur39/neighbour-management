package com.neighbourmanagement.backend.repository;

import com.neighbourmanagement.backend.entity.DeletionHistory;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;

public interface DeletionHistoryRepository
        extends JpaRepository<DeletionHistory, Long> {


    List<DeletionHistory>
    findAllByOrderByDeletedAtDesc();


    List<DeletionHistory>
    findByDeletedAtBetweenOrderByDeletedAtDesc(
            LocalDateTime start,
            LocalDateTime end
    );


    @Query("""
        SELECT COALESCE(SUM(d.deletedCount), 0)
        FROM DeletionHistory d
        WHERE d.deletedAt >= :start
        AND d.deletedAt < :end
    """)
    Long getTotalDeletedBetween(
            @Param("start")
            LocalDateTime start,

            @Param("end")
            LocalDateTime end
    );
}