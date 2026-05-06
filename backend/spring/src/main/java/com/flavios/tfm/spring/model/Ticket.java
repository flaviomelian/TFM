package com.flavios.tfm.spring.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "tickets")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Ticket {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(columnDefinition = "TEXT", nullable = false)
    private String userText;

    private String predictedCategory;

    private Double confidence;

    @Column(columnDefinition = "TEXT")
    private String aiResponse;

    private LocalDateTime createdAt = LocalDateTime.now();

    // Cambiado de Boolean a Enum con valor por defecto
    @Enumerated(EnumType.STRING)
    private ValidationStatus validated = ValidationStatus.PENDING;

    private String correctedCategory;
}