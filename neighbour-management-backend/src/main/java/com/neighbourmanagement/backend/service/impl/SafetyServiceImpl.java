package com.neighbourmanagement.backend.service.impl;

import com.neighbourmanagement.backend.dto.safety.SafetyDecisionResponse;
import com.neighbourmanagement.backend.dto.validation.ValidationResponse;
import com.neighbourmanagement.backend.dto.validation.ValidationResultResponse;
import com.neighbourmanagement.backend.service.SafetyService;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class SafetyServiceImpl implements SafetyService {

    @Override
    public SafetyDecisionResponse evaluate(
            ValidationResponse validationResponse,
            Integer minimumNeighbours
    ) {

        // =====================================================
        // BASIC VALIDATION
        // =====================================================

        if (validationResponse == null) {
            throw new IllegalArgumentException(
                    "Validation response cannot be null"
            );
        }

        if (
                validationResponse.getTotalNeighbours() == null
                        || validationResponse.getValidNeighbours() == null
                        || validationResponse.getInvalidNeighbours() == null
        ) {
            throw new IllegalArgumentException(
                    "Validation counts cannot be null"
            );
        }

        if (minimumNeighbours == null || minimumNeighbours < 1) {
            minimumNeighbours = 1;
        }


        // =====================================================
        // GET VALIDATION COUNTS
        // =====================================================

        int total =
                validationResponse.getTotalNeighbours();

        int valid =
                validationResponse.getValidNeighbours();

        int invalid =
                validationResponse.getInvalidNeighbours();


        // =====================================================
        // GET VALID AND INVALID NEIGHBOUR IDs
        // =====================================================

        List<Long> validIds =
                getValidNeighbourIds(
                        validationResponse
                );

        List<Long> invalidIds =
                getInvalidNeighbourIds(
                        validationResponse
                );


        // =====================================================
        // SAFETY CONSISTENCY CHECK
        // =====================================================
        //
        // The reported validation counts and actual result IDs
        // must agree before deletion is allowed.
        //
        // This prevents an inconsistent validation response
        // from accidentally causing unsafe deletion.
        //
        // =====================================================

        int resultCount =
                validIds.size() + invalidIds.size();

        if (resultCount != total) {

            throw new IllegalStateException(
                    "Validation result count does not match "
                            + "total neighbour count"
            );
        }

        if (validIds.size() != valid) {

            throw new IllegalStateException(
                    "Valid neighbour count does not match "
                            + "validation results"
            );
        }

        if (invalidIds.size() != invalid) {

            throw new IllegalStateException(
                    "Invalid neighbour count does not match "
                            + "validation results"
            );
        }


        // =====================================================
        // PREPARE SAFETY DECISION
        // =====================================================

        List<Long> neighboursToDelete =
                new ArrayList<>();

        List<Long> neighboursToRetain =
                new ArrayList<>();


        // =====================================================
        // CASE 1
        // SOME NEIGHBOURS ARE VALID
        // =====================================================
        //
        // Minimum retention DOES NOT apply here.
        //
        // All valid neighbours are retained.
        // All invalid neighbours are eligible for deletion.
        //
        // =====================================================

        if (valid > 0) {

            // -------------------------------------------------
            // Retain all valid neighbours
            // -------------------------------------------------

            neighboursToRetain.addAll(
                    validIds
            );


            // -------------------------------------------------
            // Delete all invalid neighbours
            // -------------------------------------------------

            neighboursToDelete.addAll(
                    invalidIds
            );
        }


        // =====================================================
        // CASE 2
        // ALL NEIGHBOURS ARE INVALID
        // =====================================================
        //
        // Minimum retention applies ONLY in this case.
        //
        // Example:
        //
        // Total   = 10
        // Valid   = 0
        // Invalid = 10
        // Minimum = 5
        //
        // Retain 5 invalid neighbours.
        // Delete remaining 5.
        //
        // =====================================================

        else if (
                total > 0
                        && invalid == total
        ) {

            int retainCount =
                    Math.min(
                            minimumNeighbours,
                            invalidIds.size()
                    );


            // -------------------------------------------------
            // Retain minimum number of invalid neighbours
            // -------------------------------------------------

            for (
                    int i = 0;
                    i < retainCount;
                    i++
            ) {

                neighboursToRetain.add(
                        invalidIds.get(i)
                );
            }


            // -------------------------------------------------
            // Delete remaining invalid neighbours
            // -------------------------------------------------

            for (
                    int i = retainCount;
                    i < invalidIds.size();
                    i++
            ) {

                neighboursToDelete.add(
                        invalidIds.get(i)
                );
            }
        }


        // =====================================================
        // CASE 3
        // NO INVALID NEIGHBOURS
        // =====================================================
        //
        // All neighbours are valid.
        //
        // Nothing is deleted.
        //
        // =====================================================

        else {

            neighboursToDelete.clear();

            neighboursToRetain.addAll(
                    validIds
            );
        }


        // =====================================================
        // FINAL SAFETY CHECK
        // =====================================================
        //
        // If every neighbour is invalid, the final retained
        // count must never be below the configured minimum,
        // whenever the total number of neighbours is large
        // enough to satisfy that minimum.
        //
        // =====================================================

        if (
                total > 0
                        && invalid == total
                        && neighboursToRetain.size()
                        < Math.min(
                                minimumNeighbours,
                                total
                        )
        ) {

            throw new IllegalStateException(
                    "Safety rule violation: minimum neighbour "
                            + "retention requirement was not satisfied"
            );
        }


        // =====================================================
        // BUILD SAFETY RESPONSE
        // =====================================================

        SafetyDecisionResponse response =
                new SafetyDecisionResponse();


        response.setTotalNeighbours(
                total
        );

        response.setValidNeighbours(
                valid
        );

        response.setInvalidNeighbours(
                invalid
        );

        response.setMinimumNeighbours(
                minimumNeighbours
        );


        response.setNeighboursToDelete(
                neighboursToDelete.size()
        );

        response.setNeighboursToRetain(
                neighboursToRetain.size()
        );


        // =====================================================
        // DELETION PERMISSION
        // =====================================================
        //
        // Deletion is allowed only when the safety engine has
        // identified at least one neighbour that is safe to
        // delete.
        //
        // This method does NOT perform deletion.
        //
        // =====================================================

        response.setDeletionAllowed(
                !neighboursToDelete.isEmpty()
        );


        response.setNeighbourIdsToDelete(
                neighboursToDelete
        );

        response.setNeighbourIdsToRetain(
                neighboursToRetain
        );


        return response;
    }


    // =========================================================
    // GET VALID NEIGHBOUR IDs
    // =========================================================

    private List<Long> getValidNeighbourIds(
            ValidationResponse validationResponse
    ) {

        if (
                validationResponse.getResults() == null
                        || validationResponse
                        .getResults()
                        .isEmpty()
        ) {

            return new ArrayList<>();
        }


        List<Long> validIds =
                new ArrayList<>();


        for (
                ValidationResultResponse result
                : validationResponse.getResults()
        ) {

            if (
                    result != null
                            && result.getNeighbourId() != null
                            && "VALID".equalsIgnoreCase(
                            result.getStatus()
                    )
            ) {

                validIds.add(
                        result.getNeighbourId()
                );
            }
        }


        return validIds;
    }


    // =========================================================
    // GET INVALID NEIGHBOUR IDs
    // =========================================================

    private List<Long> getInvalidNeighbourIds(
            ValidationResponse validationResponse
    ) {

        if (
                validationResponse.getResults() == null
                        || validationResponse
                        .getResults()
                        .isEmpty()
        ) {

            return new ArrayList<>();
        }


        List<Long> invalidIds =
                new ArrayList<>();


        for (
                ValidationResultResponse result
                : validationResponse.getResults()
        ) {

            if (
                    result != null
                            && result.getNeighbourId() != null
                            && "INVALID".equalsIgnoreCase(
                            result.getStatus()
                    )
            ) {

                invalidIds.add(
                        result.getNeighbourId()
                );
            }
        }


        return invalidIds;
    }
}