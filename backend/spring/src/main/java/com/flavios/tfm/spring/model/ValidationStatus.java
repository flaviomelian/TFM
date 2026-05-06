package com.flavios.tfm.spring.model;

public enum ValidationStatus {
    PENDING,    // Recién llegado de la IA, sin intervención humana
    VALIDATED,  // El humano confirmó que la IA acertó
    CORRECTED   // El humano cambió la categoría manualmente
}