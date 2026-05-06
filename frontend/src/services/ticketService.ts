const API_URL = 'http://localhost:8080/api/tickets';
//const API_URL = 'tfm_spring/api/tickets';

export const ticketService = {
  // Enviar texto a Spring para que FastAPI lo clasifique
  classify: async (text: string) => {
    const response = await fetch(`${API_URL}/classify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    if (!response.ok) throw new Error('Error en la comunicación con el servidor');
    return response.json();
  },

  // Obtener historial para el Admin
  getAll: async () => {
    const response = await fetch(API_URL);
    return response.json();
  }
};