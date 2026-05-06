import tensorflow as tf
import pickle
import numpy as np
from keras.preprocessing.sequence import pad_sequences

# 1. Carga de modelo y recursos
model = tf.keras.models.load_model('models/category_model.keras')
with open('models/tokenizer.pickle', 'rb') as h:
    tokenizer = pickle.load(h)

# 2. Dataset de validación externa (Frases que el modelo NUNCA ha visto)
test_real = [
    "I'm deeply disappointed and I require a total compensation", # Esperado: Refund (0)
    "La plataforma no responde en absoluto en mi navegador",       # Esperado: Technical (1)
    "I'd like to terminate my membership right away",             # Esperado: Cancellation (2)
    "Dime la capacidad de almacenamiento de este equipo",          # Esperado: Product (3)
    "He visto un cargo que no reconozco en mi cuenta bancaria",    # Esperado: Billing (4)
    "My device is getting extremely hot when charging",           # Esperado: Technical (1)
    "¿Tenéis stock de este artículo en otros colores?",            # Esperado: Product (3)
    "I want to stop the auto-renewal of my subscription"           # Esperado: Cancellation (2)
]

# Etiquetas reales para comparar (Ground Truth)
true_labels = [0, 1, 2, 3, 4, 1, 3, 2]
categories = ["Refund/Reembolso", "Technical/Técnico", "Cancellation/Cancelación", "Product/Producto", "Billing/Facturación"]

# 3. Preprocesamiento
seq = tokenizer.texts_to_sequences(test_real)
padded = pad_sequences(seq, maxlen=150)

# 4. Predicción
print("\n--- EJECUTANDO TEST DE ESTRÉS SEMÁNTICO ---\n")
preds = model.predict(padded, verbose=0)

hits = 0
for i, probas in enumerate(preds):
    pred_idx = np.argmax(probas)
    confianza = np.max(probas) * 100
    es_correcto = pred_idx == true_labels[i]
    
    if es_correcto:
        hits += 1
        status = "✅ [ACIERTO]"
    else:
        status = "❌ [FALLO]"

    print(f"{status} Frase: '{test_real[i]}'")
    print(f"      Predicción: {categories[pred_idx]} ({confianza:.2f}% de confianza)")
    print(f"      Esperado:   {categories[true_labels[i]]}\n")

# 5. Métrica final
accuracy_final = (hits / len(test_real)) * 100
print(f"--- RESULTADO DEL TEST REAL ---")
print(f"Precisión fuera de entrenamiento: {accuracy_final}%")
print(f"Interpretación: {'Modelo Robusto' if accuracy_final > 80 else 'Overfitting detectado: el modelo memoriza pero no entiende'}")
