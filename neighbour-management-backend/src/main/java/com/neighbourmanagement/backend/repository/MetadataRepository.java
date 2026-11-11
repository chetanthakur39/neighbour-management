package com.neighbourmanagement.backend.repository;

import com.neighbourmanagement.backend.entity.ENode;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface MetadataRepository
        extends JpaRepository<ENode, Long> {

    @Query("""
        SELECT DISTINCT e.state
        FROM ENode e
        WHERE e.state IS NOT NULL
        ORDER BY e.state
    """)
    List<String> findAllStates();

    @Query("""
        SELECT DISTINCT e.jc
        FROM ENode e
        WHERE e.state = :state
        AND e.jc IS NOT NULL
        ORDER BY e.jc
    """)
    List<String> findJcsByState(
            @Param("state") String state
    );

    @Query("""
        SELECT DISTINCT e.jc
        FROM ENode e
        WHERE e.jc IS NOT NULL
        ORDER BY e.jc
    """)
    List<String> findAllJcs();

    @Query("""
        SELECT COUNT(e)
        FROM ENode e
        WHERE e.state = :state
        AND e.jc = :jc
    """)
    long countStateJc(
            @Param("state") String state,
            @Param("jc") String jc
    );
}