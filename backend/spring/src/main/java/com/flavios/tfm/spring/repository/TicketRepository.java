package com.flavios.tfm.spring.repository;

import com.flavios.tfm.spring.model.Ticket;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface TicketRepository extends JpaRepository<Ticket, Long> {
    
    // Método que usará tu CronJob para sacar datos nuevos y reentrenar
    List<Ticket> findByValidatedTrueAndCorrectedCategoryIsNotNull();

    // Método para tu panel de BI: obtener tickets por categoría
    long countByPredictedCategory(String category);
} 
