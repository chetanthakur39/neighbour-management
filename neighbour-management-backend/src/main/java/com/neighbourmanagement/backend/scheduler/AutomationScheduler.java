package com.neighbourmanagement.backend.scheduler;

import com.neighbourmanagement.backend.entity.Automation;
import com.neighbourmanagement.backend.enums.AutomationStatus;
import com.neighbourmanagement.backend.repository.AutomationRepository;
import com.neighbourmanagement.backend.service.AutomationRunService;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@Component
public class AutomationScheduler {

    private final AutomationRepository automationRepository;

    private final AutomationRunService automationRunService;


    public AutomationScheduler(
            AutomationRepository automationRepository,
            AutomationRunService automationRunService
    ) {

        this.automationRepository =
                automationRepository;

        this.automationRunService =
                automationRunService;
    }


    // =========================================================
    // CHECK EVERY MINUTE
    // =========================================================

    @Scheduled(cron = "0 * * * * *")
    public void checkScheduledAutomations() {

        LocalDate today =
                LocalDate.now();

        LocalTime currentTime =
                LocalTime.now()
                        .withSecond(0)
                        .withNano(0);


        List<Automation> automations =
                automationRepository.findAll();


        for (Automation automation : automations) {

            // -------------------------------------------------
            // Only RUNNING automations
            // -------------------------------------------------

            if (
                    automation.getStatus()
                            != AutomationStatus.RUNNING
            ) {

                continue;
            }


            // -------------------------------------------------
            // Only DAILY automations
            // -------------------------------------------------

            if (
                    automation.getFrequency() == null
                            || !"DAILY".equalsIgnoreCase(
                            automation.getFrequency()
                    )
            ) {

                continue;
            }


            // -------------------------------------------------
            // Execution time must exist
            // -------------------------------------------------

            if (
                    automation.getExecutionTime() == null
            ) {

                continue;
            }


            LocalTime executionTime =
                    automation.getExecutionTime()
                            .withSecond(0)
                            .withNano(0);


            // -------------------------------------------------
            // Has scheduled time arrived?
            // -------------------------------------------------

            if (
                    currentTime.isBefore(
                            executionTime
                    )
            ) {

                continue;
            }


            // -------------------------------------------------
            // Prevent multiple executions in same day
            // -------------------------------------------------

            if (
                    automation.getLastRunAt() != null
                            && automation.getLastRunAt()
                            .toLocalDate()
                            .equals(today)
            ) {

                continue;
            }


            // -------------------------------------------------
            // Run automation
            // -------------------------------------------------

            runAutomation(
                    automation
            );
        }
    }


    // =========================================================
    // RUN AUTOMATION
    // =========================================================

    private void runAutomation(
            Automation automation
    ) {

        try {

            System.out.println(
                    "Running scheduled automation: "
                            + automation.getAutomationId()
            );


            automationRunService.runAutomation(
                    automation.getAutomationId()
            );


            System.out.println(
                    "Scheduled automation completed: "
                            + automation.getAutomationId()
            );

        } catch (Exception exception) {

            System.err.println(
                    "Scheduled automation failed: "
                            + automation.getAutomationId()
            );

            System.err.println(
                    exception.getMessage()
            );
        }
    }
}