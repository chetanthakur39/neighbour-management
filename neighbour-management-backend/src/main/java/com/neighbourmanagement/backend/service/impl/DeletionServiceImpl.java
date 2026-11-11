package com.neighbourmanagement.backend.service.impl;

import com.neighbourmanagement.backend.dto.deletion.DeletionRequest;
import com.neighbourmanagement.backend.repository.NeighbourRepository;
import com.neighbourmanagement.backend.service.DeletionHistoryService;
import com.neighbourmanagement.backend.service.DeletionService;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class DeletionServiceImpl
        implements DeletionService {

    private final NeighbourRepository
            neighbourRepository;

    private final DeletionHistoryService
            deletionHistoryService;


    // =========================================================
    // CONSTRUCTOR
    // =========================================================

    public DeletionServiceImpl(
            NeighbourRepository neighbourRepository,
            DeletionHistoryService deletionHistoryService
    ) {

        this.neighbourRepository =
                neighbourRepository;

        this.deletionHistoryService =
                deletionHistoryService;
    }


    // =========================================================
    // DEFAULT DELETION
    //
    // Direct chatbot deletion.
    // =========================================================

    @Override
    @Transactional
    public int deleteNeighbours(
            DeletionRequest request
    ) {

        return deleteNeighbours(
                request,
                "CHATBOT"
        );
    }


    // =========================================================
    // SOURCE-AWARE DELETION
    //
    // CHATBOT
    // AUTOMATION
    // =========================================================

    @Override
    @Transactional
    public int deleteNeighbours(
            DeletionRequest request,
            String source
    ) {

        // =====================================================
        // BASIC VALIDATION
        // =====================================================

        if (request == null) {

            throw new IllegalArgumentException(
                    "Deletion request cannot be null"
            );
        }


        if (
                request.getState() == null
                        || request.getState().isBlank()
        ) {

            throw new IllegalArgumentException(
                    "State is required"
            );
        }


        if (
                request.getJc() == null
                        || request.getJc().isBlank()
        ) {

            throw new IllegalArgumentException(
                    "JC is required"
            );
        }


        if (
                request.getNeighbourIds() == null
                        || request.getNeighbourIds().isEmpty()
        ) {

            return 0;
        }


        // =====================================================
        // VALIDATE SOURCE
        // =====================================================

        if (
                source == null
                        || source.isBlank()
        ) {

            source = "CHATBOT";
        }


        source = source.trim().toUpperCase();


        if (
                !"CHATBOT".equals(source)
                        && !"AUTOMATION".equals(source)
        ) {

            throw new IllegalArgumentException(
                    "Invalid deletion source: "
                            + source
            );
        }


        // =====================================================
        // VERIFY REQUESTED IDs
        //
        // Only IDs belonging to the requested State + JC
        // can be deleted.
        // =====================================================

        List<Long> verifiedIds =
                neighbourRepository
                        .findNeighbourIdsForStateAndJc(
                                request.getState(),
                                request.getJc(),
                                request.getNeighbourIds()
                        );


        if (verifiedIds.isEmpty()) {

            throw new IllegalArgumentException(
                    "None of the requested neighbours "
                            + "belong to the specified "
                            + "State and JC"
            );
        }


        // =====================================================
        // DELETE ONLY VERIFIED IDs
        // =====================================================

        neighbourRepository
                .deleteByNeighbourIdIn(
                        verifiedIds
                );


        int deletedCount =
                verifiedIds.size();


        // =====================================================
        // RECORD DELETION HISTORY
        //
        // This records BOTH:
        //
        // CHATBOT
        // AUTOMATION
        //
        // in the same deletion_history table.
        // =====================================================

        deletionHistoryService.recordDeletion(
                request.getState(),
                request.getJc(),
                deletedCount,
                request.getMinimumNeighbours(),
                source
        );


        // =====================================================
        // RETURN DELETED COUNT
        // =====================================================

        return deletedCount;
    }
}