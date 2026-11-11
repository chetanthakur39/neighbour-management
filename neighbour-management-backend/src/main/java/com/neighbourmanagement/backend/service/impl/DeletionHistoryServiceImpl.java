package com.neighbourmanagement.backend.service.impl;

import com.neighbourmanagement.backend.entity.DeletionHistory;
import com.neighbourmanagement.backend.repository.DeletionHistoryRepository;
import com.neighbourmanagement.backend.service.DeletionHistoryService;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;

@Service
public class DeletionHistoryServiceImpl
        implements DeletionHistoryService {

    private final DeletionHistoryRepository
            deletionHistoryRepository;


    public DeletionHistoryServiceImpl(
            DeletionHistoryRepository
                    deletionHistoryRepository
    ) {

        this.deletionHistoryRepository =
                deletionHistoryRepository;
    }


    // =========================================================
    // RECORD DELETION
    // =========================================================

    @Override
    @Transactional
    public DeletionHistory recordDeletion(
            String state,
            String jc,
            Integer deletedCount,
            Integer minimumNeighbours,
            String source
    ) {

        if (
                state == null
                        || state.isBlank()
        ) {

            throw new IllegalArgumentException(
                    "State is required"
            );
        }


        if (
                jc == null
                        || jc.isBlank()
        ) {

            throw new IllegalArgumentException(
                    "JC is required"
            );
        }


        if (
                deletedCount == null
                        || deletedCount < 1
        ) {

            throw new IllegalArgumentException(
                    "Deleted count must be greater than zero"
            );
        }


        if (
                source == null
                        || source.isBlank()
        ) {

            throw new IllegalArgumentException(
                    "Deletion source is required"
            );
        }


        source =
                source.trim().toUpperCase();


        if (
                !"CHATBOT".equals(source)
                        && !"AUTOMATION".equals(source)
        ) {

            throw new IllegalArgumentException(
                    "Invalid deletion source: "
                            + source
            );
        }


        DeletionHistory history =
                new DeletionHistory();


        history.setState(state);

        history.setJc(jc);

        history.setDeletedCount(
                deletedCount
        );

        history.setMinimumNeighbours(
                minimumNeighbours
        );

        history.setSource(
                source
        );

        history.setDeletedAt(
                LocalDateTime.now()
        );


        return deletionHistoryRepository.save(
                history
        );
    }


    // =========================================================
    // ALL HISTORY
    // =========================================================

    @Override
    @Transactional(readOnly = true)
    public List<DeletionHistory>
    getAllHistory() {

        return deletionHistoryRepository
                .findAllByOrderByDeletedAtDesc();
    }


    // =========================================================
    // HISTORY FOR DATE
    // =========================================================

    @Override
    @Transactional(readOnly = true)
    public List<DeletionHistory>
    getHistoryForDate(
            LocalDate date
    ) {

        LocalDateTime start =
                LocalDateTime.of(
                        date,
                        LocalTime.MIN
                );


        LocalDateTime end =
                start.plusDays(1);


        return deletionHistoryRepository
                .findByDeletedAtBetweenOrderByDeletedAtDesc(
                        start,
                        end
                );
    }


    // =========================================================
    // TOTAL DELETED FOR DATE
    // =========================================================

    @Override
    @Transactional(readOnly = true)
    public Long getTotalDeletedForDate(
            LocalDate date
    ) {

        LocalDateTime start =
                LocalDateTime.of(
                        date,
                        LocalTime.MIN
                );


        LocalDateTime end =
                start.plusDays(1);


        return deletionHistoryRepository
                .getTotalDeletedBetween(
                        start,
                        end
                );
    }
}