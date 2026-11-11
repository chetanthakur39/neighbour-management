package com.neighbourmanagement.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class NeighbourManagementBackendApplication {

    public static void main(String[] args) {

        SpringApplication.run(
                NeighbourManagementBackendApplication.class,
                args
        );
    }
}