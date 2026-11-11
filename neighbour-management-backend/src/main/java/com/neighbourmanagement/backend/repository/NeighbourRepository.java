package com.neighbourmanagement.backend.repository;

import com.neighbourmanagement.backend.entity.Neighbour;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface NeighbourRepository
        extends JpaRepository<Neighbour, Long> {

    @Query("""
        SELECT n
        FROM Neighbour n
        JOIN ECell e
            ON n.ecellId = e.ecellId
        JOIN ENode en
            ON e.enodeId = en.enodeId
        WHERE en.state = :state
        AND en.jc = :jc
    """)
    List<Neighbour> findByStateAndJc(
            @Param("state") String state,
            @Param("jc") String jc
    );


    void deleteByNeighbourIdIn(
            List<Long> neighbourIds
    );


    @Query("""
        SELECT n.neighbourId
        FROM Neighbour n
        JOIN ECell e
            ON n.ecellId = e.ecellId
        JOIN ENode en
            ON e.enodeId = en.enodeId
        WHERE en.state = :state
        AND en.jc = :jc
        AND n.neighbourId IN :neighbourIds
    """)
    List<Long> findNeighbourIdsForStateAndJc(
            @Param("state") String state,
            @Param("jc") String jc,
            @Param("neighbourIds") List<Long> neighbourIds
    );
}