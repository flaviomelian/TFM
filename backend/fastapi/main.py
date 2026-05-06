from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import pickle
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import ollama
import subprocess
import time
import httpx
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Lanzamos el proceso de Ollama en el host
    print("🚀 Iniciando Ollama Serve...")
    proc = subprocess.Popen(
        ["ollama", "serve"], 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    
    # 2. Espera activa: Intentamos conectar hasta que responda (máximo 10 seg)
    retries = 5
    connected = False
    while retries > 0:
        try:
            # Comprobamos si el puerto 11434 ya acepta peticiones
            with httpx.Client() as client:
                resp = client.get("http://localhost:11434/")
                if resp.status_code == 200:
                    print("✅ Ollama está listo y respondiendo.")
                    connected = True
                    break
        except Exception:
            print(f"⏳ Esperando a Ollama... (Reintentos: {retries})")
            time.sleep(2)
            retries -= 1
            
    if not connected:
        print("⚠️ Advertencia: Ollama no arrancó a tiempo. Revisa si el modelo 'llama3' existe.")
    
    yield

# --- LÓGICA DE ARRANQUE ASÍNCRONO ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto se ejecuta al iniciar la API
    print("Iniciando servicio de Ollama...")
    try:
        # Lanzamos 'ollama serve' como un proceso independiente
        # stdout y stderr a DEVNULL para no ensuciar tu consola de FastAPI
        subprocess.Popen(["ollama", "serve"], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        # Damos un par de segundos para que el servidor levante
        time.sleep(2) 
        print("Servicio Ollama verificado.")
    except Exception as e:
        print(f"No se pudo iniciar Ollama automáticamente: {e}")
    
    yield
    # Aquí podrías añadir lógica para cerrar procesos al apagar la API si quisieras

app = FastAPI(title="AI Expert Support API", version="3.1", lifespan=lifespan)

# --- CARGA DE RECURSOS ---
model = tf.keras.models.load_model('models/category_model.keras')
with open('models/tokenizer.pickle', 'rb') as h:
    tokenizer = pickle.load(h)

categories = ["Refund/Reembolso", "Technical/Técnico", "Cancellation/Cancelación", "Product/Producto", "Billing/Facturación"]

class Ticket(BaseModel):
    text: str

@app.post("/predict")
async def predict_category(ticket: Ticket):
    try:
        texto_usuario = ticket.text.lower()
        
        # 1. Inferencia CNN
        seq = tokenizer.texts_to_sequences([texto_usuario])
        padded = pad_sequences(seq, maxlen=150)
        prediction = model.predict(padded, verbose=0)
        final_idx = int(np.argmax(prediction))
        categoria_final = categories[final_idx]

        # 2. Llamada a Ollama LOCAL
        prompt = f"Responde como soporte técnico a: '{ticket.text}'. Categoría: {categoria_final}. Máximo 2 frases."
        
        try:
            # Subimos el timeout a 60 segundos por si tu CPU va lenta cargando el modelo
            client = ollama.Client(host='http://localhost:11434', timeout=60.0) 
            
            response = client.chat(model='llama3.2:latest', messages=[
                {'role': 'user', 'content': prompt}
            ])
            ai_gen_response = response['message']['content']
            
        except Exception as ollama_err:
            # ESTO ES CLAVE: Mira tu terminal de Python para ver el error real
            print(f"--- ERROR REAL DE OLLAMA: {ollama_err} ---")
            
            # Si el error es que no encuentra el modelo, cámbialo a uno que tengas
            # o haz un 'ollama pull llama3'
            ai_gen_response = f"Incidencia registrada como {categoria_final}. (Error: {str(ollama_err)[:50]}...)"

        return {
            "category": categoria_final,
            "confidence": f"{float(np.max(prediction)):.2%}",
            "ai_response": ai_gen_response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))