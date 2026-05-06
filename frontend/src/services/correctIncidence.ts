// El DTO que espera el backend
export interface TicketCorrectionRequest {
  correctedCategory: string;
}

// La interfaz del Ticket para tener autocompletado en el objeto 't'
export interface Ticket {
  id: number;
  userText: string;
  predictedCategory: string;
  confidence: number;
  aiResponse: string;
  createdAt: string;
  validated: boolean;
  correctedCategory?: string;
}

export const correctIncidence = async (
  id: number, 
  feedback: string, 
  t: Ticket
): Promise<Ticket | null> => {
  try {
    const response = await fetch(`http://tu-ip-nodo-2:8080/api/tickets/${id}/validate`, {
      method: 'PATCH',
      headers: { 
        'Content-Type': 'application/json' 
      },
      body: JSON.stringify({ 
        // Si hay feedback (corrección), lo enviamos. 
        // Si no (clic en "Correcto"), enviamos la predicción original.
        correctedCategory: feedback || t.predictedCategory 
      } as TicketCorrectionRequest)
    });

    if (!response.ok) {
      throw new Error(`Error en la validación: ${response.statusText}`);
    }

    const updatedTicket: Ticket = await response.json();
    return updatedTicket;

  } catch (error) {
    console.error("Fallo al conectar con el servidor de Spring:", error);
    alert("No se pudo conectar con el servidor para validar el ticket.");
    return null;
  }
};