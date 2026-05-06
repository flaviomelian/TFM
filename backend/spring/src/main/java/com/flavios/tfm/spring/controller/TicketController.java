package com.flavios.tfm.spring.controller;

import com.flavios.tfm.spring.dto.TicketCorrectionRequest;
import com.flavios.tfm.spring.dto.TicketRequest;
import com.flavios.tfm.spring.model.Ticket;
import com.flavios.tfm.spring.service.TicketService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/tickets")
@Tag(name = "Tickets", description = "Endpoint para procesar incidencias con IA")
@CrossOrigin(origins = "*") // Para que Next.js no te dé problemas de CORS en desarrollo
public class TicketController {

    private final TicketService ticketService;

    public TicketController(TicketService ticketService) {
        this.ticketService = ticketService;
    }

    @GetMapping
    @Operation(summary = "Obtener todos los tickets registrados")
    public ResponseEntity<List<Ticket>> getAllTickets() {
        return ResponseEntity.ok(ticketService.getAllTickets());
    }

    @PostMapping("/classify")
    @Operation(summary = "Enviar incidencia a la IA y guardar en BD")
    public ResponseEntity<Ticket> classifyTicket(@RequestBody TicketRequest request) {
        Ticket savedTicket = ticketService.processAndSaveTicket(request);
        return ResponseEntity.ok(savedTicket);
    }

    @PatchMapping("/{id}/validate")
    @Operation(summary = "Valida o corrige la categoría de un ticket")
    public ResponseEntity<Ticket> validateTicket(
            @PathVariable Long id, 
            @RequestBody TicketCorrectionRequest correction) {
        
        Ticket updatedTicket = ticketService.validateAndCorrectTicket(id, correction.getCorrectedCategory());
        return ResponseEntity.ok(updatedTicket);
    }
}