package com.neighbourmanagement.backend.service;

import com.neighbourmanagement.backend.dto.deletion.DeletionRequest;

public interface DeletionService {

    // =========================================================
    // DEFAULT DELETION
    //
    // Used by direct chatbot cleanup.
    // Source defaults to CHATBOT.
    // =========================================================

    int deleteNeighbours(
            DeletionRequest request
    );


    // =========================================================
    // SOURCE-AWARE DELETION
    //
    // Supported sources:
    //
    // CHATBOT
    // AUTOMATION
    // =========================================================

    int deleteNeighbours(
            DeletionRequest request,
            String source
    );
}