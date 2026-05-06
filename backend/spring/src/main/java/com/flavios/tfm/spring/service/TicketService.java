package com.flavios.tfm.spring.service;

import com.flavios.tfm.spring.dto.TicketRequest;
import com.flavios.tfm.spring.model.Ticket;
import com.flavios.tfm.spring.model.ValidationStatus;
import com.flavios.tfm.spring.repository.TicketRepository;

import io.github.cdimascio.dotenv.Dotenv;
import jakarta.transaction.Transactional;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import java.util.Map;
import java.util.List;

@Service
public class TicketService {

    private final TicketRepository ticketRepository;
    private final WebClient webClient;

    public TicketService(TicketRepository ticketRepository, WebClient.Builder webClientBuilder) {
        this.ticketRepository = ticketRepository;
        // La URL de tu FastAPI (Uvicorn)
        this.webClient = webClientBuilder.baseUrl(Dotenv.load().get("FASTAPI_URL")).build();
    }

    public List<Ticket> getAllTickets() {
        return ticketRepository.findAll();
    }

    public Ticket processAndSaveTicket(TicketRequest request) {
        // 1. Llamada a FastAPI (asumimos que devuelve un Map o un DTO de respuesta)
        // Usamos .block() para simplificar el flujo síncrono inicial,
        // pero al usar WebClient ya estás preparado para hacerlo reactivo si creces.
        Map<String, Object> aiResponse = webClient.post()
                .uri("/predict")
                .bodyValue(Map.of("text", request.getText()))
                .retrieve()
                .bodyToMono(new ParameterizedTypeReference<Map<String, Object>>() {
                })
                .block();

        // 2. Mapear la respuesta de la IA a nuestra Entidad
        Ticket ticket = new Ticket();
        ticket.setUserText(request.getText());

        if (aiResponse != null) {
            ticket.setPredictedCategory((String) aiResponse.get("category"));

            // Solución robusta para el error de casting
            Object confidenceObj = aiResponse.get("confidence");
            if (confidenceObj != null)
                ticket.setConfidence(Double
                        .parseDouble(confidenceObj.toString().substring(0, confidenceObj.toString().length() - 1)));

            ticket.setAiResponse((String) aiResponse.get("ai_response"));
        }

        // 3. Persistir en MySQL
        return ticketRepository.save(ticket);
    }

    @Transactional
    public Ticket validateAndCorrectTicket(Long id, String correctedCategoryFromFront) {
        Ticket ticket = ticketRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Ticket no encontrado"));

        // Comparamos lo que llega del front con lo que predijo la IA
        if (correctedCategoryFromFront != null &&
                !correctedCategoryFromFront.equalsIgnoreCase(ticket.getPredictedCategory())) {

            ticket.setCorrectedCategory(correctedCategoryFromFront);
            ticket.setValidated(ValidationStatus.CORRECTED);
        } else {
            // El operario dio el visto bueno a la predicción original
            ticket.setCorrectedCategory(ticket.getPredictedCategory());
            ticket.setValidated(ValidationStatus.VALIDATED);
        }

        return ticketRepository.save(ticket);
    }
}
