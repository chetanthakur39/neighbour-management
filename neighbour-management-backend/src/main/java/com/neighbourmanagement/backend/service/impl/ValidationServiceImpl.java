package com.neighbourmanagement.backend.service.impl;

import com.neighbourmanagement.backend.dto.validation.ValidationRequest;
import com.neighbourmanagement.backend.dto.validation.ValidationResponse;
import com.neighbourmanagement.backend.dto.validation.ValidationResultResponse;
import com.neighbourmanagement.backend.entity.FourGConfiguration;
import com.neighbourmanagement.backend.entity.FiveGConfiguration;
import com.neighbourmanagement.backend.entity.Neighbour;
import com.neighbourmanagement.backend.enums.AutomationRuleType;
import com.neighbourmanagement.backend.repository.FourGConfigurationRepository;
import com.neighbourmanagement.backend.repository.FiveGConfigurationRepository;
import com.neighbourmanagement.backend.repository.NeighbourRepository;
import com.neighbourmanagement.backend.service.ValidationService;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;

@Service
@Transactional(readOnly = true)
public class ValidationServiceImpl implements ValidationService {

    private final NeighbourRepository neighbourRepository;

    private final FourGConfigurationRepository fourGConfigurationRepository;

    private final FiveGConfigurationRepository fiveGConfigurationRepository;


    // =========================================================
    // CONSTRUCTOR
    // =========================================================

    public ValidationServiceImpl(
            NeighbourRepository neighbourRepository,
            FourGConfigurationRepository fourGConfigurationRepository,
            FiveGConfigurationRepository fiveGConfigurationRepository
    ) {

        this.neighbourRepository = neighbourRepository;
        this.fourGConfigurationRepository =
                fourGConfigurationRepository;
        this.fiveGConfigurationRepository =
                fiveGConfigurationRepository;
    }


    // =========================================================
    // RUN VALIDATION
    // =========================================================

    @Override
    public ValidationResponse runValidation(
            ValidationRequest request
    ) {

        validateRequest(request);


        // -----------------------------------------------------
        // Find neighbours for selected State + JC
        // -----------------------------------------------------

        List<Neighbour> neighbours =
                neighbourRepository.findByStateAndJc(
                        request.getState(),
                        request.getJc()
                );


        List<ValidationResultResponse> results =
                new ArrayList<>();


        int validCount = 0;

        int invalidCount = 0;


        // -----------------------------------------------------
        // Validate every neighbour
        // -----------------------------------------------------

        for (Neighbour neighbour : neighbours) {

            ValidationResultResponse result =
                    validateNeighbour(
                            neighbour,
                            request.getRules()
                    );


            results.add(result);


            if ("VALID".equals(result.getStatus())) {

                validCount++;

            } else {

                invalidCount++;
            }
        }


        // -----------------------------------------------------
        // Build response
        // -----------------------------------------------------

        ValidationResponse response =
                new ValidationResponse();


        response.setState(
                request.getState()
        );

        response.setJc(
                request.getJc()
        );

        response.setTotalNeighbours(
                neighbours.size()
        );

        response.setValidNeighbours(
                validCount
        );

        response.setInvalidNeighbours(
                invalidCount
        );

        response.setResults(
                results
        );


        return response;
    }


    // =========================================================
    // VALIDATE ONE NEIGHBOUR
    // =========================================================

    private ValidationResultResponse validateNeighbour(
            Neighbour neighbour,
            List<AutomationRuleType> rules
    ) {

        List<String> failedRules =
                new ArrayList<>();


        // -----------------------------------------------------
        // Get 4G configuration
        // -----------------------------------------------------

        FourGConfiguration sourceConfiguration =
                fourGConfigurationRepository
                        .findByEcellId(
                                neighbour.getEcellId()
                        )
                        .orElse(null);


        // -----------------------------------------------------
        // Get 5G configuration
        // -----------------------------------------------------

        FiveGConfiguration targetConfiguration =
                fiveGConfigurationRepository
                        .findByGcellId(
                                neighbour.getGcellId()
                        )
                        .orElse(null);


        // -----------------------------------------------------
        // PCI VALIDATION
        // -----------------------------------------------------

        if (
                rules.contains(
                        AutomationRuleType.PCI
                )
        ) {

            if (
                    !isPciValid(
                            sourceConfiguration,
                            targetConfiguration
                    )
            ) {

                failedRules.add("PCI");
            }
        }


        // -----------------------------------------------------
        // TAC VALIDATION
        // -----------------------------------------------------

        if (
                rules.contains(
                        AutomationRuleType.TAC
                )
        ) {

            if (
                    !isTacValid(
                            sourceConfiguration,
                            targetConfiguration
                    )
            ) {

                failedRules.add("TAC");
            }
        }


        // -----------------------------------------------------
        // Build result
        // -----------------------------------------------------

        ValidationResultResponse result =
                new ValidationResultResponse();


        result.setNeighbourId(
                neighbour.getNeighbourId()
        );


        // Source / Target cell names

        result.setSourceCell(
                neighbour.getSourceCell()
        );

        result.setTargetCell(
                neighbour.getTargetCell()
        );


        // -----------------------------------------------------
        // Return REAL PCI/TAC values from configuration
        // -----------------------------------------------------

        if (sourceConfiguration != null) {

            result.setSourcePci(
                    sourceConfiguration.getPci()
            );

            result.setSourceTac(
                    sourceConfiguration.getTac()
            );

        } else {

            result.setSourcePci(null);

            result.setSourceTac(null);
        }


        if (targetConfiguration != null) {

            result.setTargetPci(
                    targetConfiguration.getPci()
            );

            result.setTargetTac(
                    targetConfiguration.getTac()
            );

        } else {

            result.setTargetPci(null);

            result.setTargetTac(null);
        }


        // -----------------------------------------------------
        // Final status
        // -----------------------------------------------------

        if (failedRules.isEmpty()) {

            result.setStatus(
                    "VALID"
            );

        } else {

            result.setStatus(
                    "INVALID"
            );
        }


        result.setFailedRules(
                failedRules
        );


        return result;
    }


    // =========================================================
    // PCI VALIDATION
    // =========================================================
    //
    // For now:
    //
    // Same PCI  -> INVALID
    // Different PCI -> VALID
    //
    // Missing configuration/PCI -> INVALID
    //
    // =========================================================

    private boolean isPciValid(
            FourGConfiguration source,
            FiveGConfiguration target
    ) {

        if (
                source == null
                        || target == null
        ) {

            return false;
        }


        Integer sourcePci =
                source.getPci();

        Integer targetPci =
                target.getPci();


        if (
                sourcePci == null
                        || targetPci == null
        ) {

            return false;
        }


        return sourcePci.equals(
                targetPci
        );
    }


    // =========================================================
    // TAC VALIDATION
    // =========================================================
    //
    // For now:
    //
    // Same TAC -> VALID
    // Different TAC -> INVALID
    //
    // Missing configuration/TAC -> INVALID
    //
    // =========================================================

    private boolean isTacValid(
            FourGConfiguration source,
            FiveGConfiguration target
    ) {

        if (
                source == null
                        || target == null
        ) {

            return false;
        }


        Integer sourceTac =
                source.getTac();

        Integer targetTac =
                target.getTac();


        if (
                sourceTac == null
                        || targetTac == null
        ) {

            return false;
        }


        return sourceTac.equals(
                targetTac
        );
    }


    // =========================================================
    // REQUEST VALIDATION
    // =========================================================

    private void validateRequest(
            ValidationRequest request
    ) {

        if (request == null) {

            throw new IllegalArgumentException(
                    "Validation request cannot be null"
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
                request.getRules() == null
                        || request.getRules().isEmpty()
        ) {

            throw new IllegalArgumentException(
                    "At least one validation rule is required"
            );
        }


        // -----------------------------------------------------
        // Only PCI and TAC are currently supported
        // -----------------------------------------------------

        for (
                AutomationRuleType rule
                : request.getRules()
        ) {

            if (
                    rule != AutomationRuleType.PCI
                            && rule != AutomationRuleType.TAC
            ) {

                throw new IllegalArgumentException(
                        "Only PCI and TAC validation rules are supported"
                );
            }
        }
    }
}