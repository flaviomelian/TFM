import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import StratifiedKFold
from gensim.models import KeyedVectors
import pickle
import os

# ==============================================================================
#  CATEGORIAS (Mapeo Sagrado - NO CAMBIAR):
#  {0: "Refund", 1: "Technical", 2: "Cancellation", 3: "Product", 4: "Billing"}
# ==============================================================================

# --- CONFIGURACIÓN INICIAL ---
if not os.path.exists('models'): 
    os.makedirs('models')

max_words = 10000
max_len = 150 
embedding_dim = 100

# 1. CARGAR DATOS
print("Cargando dataset...")
df = pd.read_csv('dataset/cleaned_data.csv').dropna()
# Mezclar el dataframe antes de hacer nada
df = df.sample(frac=1).reset_index(drop=True)
# REDUCCIÓN CONTROLADA: Para evitar el overfitting por repetición de frases
# Usamos 500 por categoría para que el modelo "sude" y aprenda patrones reales
df = df.groupby('category_label').sample(n=1000, random_state=42).reset_index(drop=True)

X = df['full_text'].astype(str).values
y = df['category_label'].astype(int).values

# 2. TOKENIZACIÓN
print("Tokenizando textos...")
tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
tokenizer.fit_on_texts(X)
X_seq = pad_sequences(tokenizer.texts_to_sequences(X), maxlen=max_len, padding='post')

# 3. CARGAR VECTORES GLOVE
print("Cargando vectores GloVe 100d...")
try:
    word_vectors = KeyedVectors.load_word2vec_format('glove.6B/glove.6B.100d.txt', binary=False, no_header=True)
except Exception as e:
    print(f"Error crítico cargando GloVe: {e}")
    exit()

# 4. CONSTRUIR MATRIZ DE EMBEDDING
print("Construyendo matriz de pesos semánticos...")
embedding_matrix = np.zeros((max_words, embedding_dim))
for word, i in tokenizer.word_index.items():
    if i < max_words:
        if word in word_vectors:
            embedding_matrix[i] = word_vectors[word]
        else:
            embedding_matrix[i] = np.random.normal(scale=0.1, size=(embedding_dim,))

# 5. VALIDACIÓN CRUZADA Y ENTRENAMIENTO
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = []

print(f"\nIniciando entrenamiento (Robust GRU con Dropout Selectivo)...")

for fold, (train_idx, val_idx) in enumerate(kfold.split(X_seq, y), 1):
    print(f"\n--- ENTRENANDO FOLD {fold} ---")
    
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(
            max_words, 
            embedding_dim, 
            weights=[embedding_matrix], 
            input_length=max_len, 
            trainable=True  
        ),
        tf.keras.layers.SpatialDropout1D(0.4),
        
        # CAPA 1: Añadimos return_sequences=True para que pase la secuencia a la siguiente
        tf.keras.layers.Bidirectional(tf.keras.layers.GRU(64, return_sequences=True)), 
        
        # CAPA 2: Esta ya puede ser False (por defecto) porque va directa a la capa Dense
        tf.keras.layers.Bidirectional(tf.keras.layers.GRU(32, return_sequences=False)), 
        
        tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.02)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(5, activation='softmax')
    ])
    
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0005)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', 
        patience=2, 
        restore_best_weights=True
    )

    model.fit(
        X_seq[train_idx], y[train_idx], 
        validation_data=(X_seq[val_idx], y[val_idx]),
        epochs=5,
        batch_size=32, # Batch más pequeño para actualizar pesos más veces con menos datos
        callbacks=[early_stop],
        verbose=1
    )
    
    scores = model.evaluate(X_seq[val_idx], y[val_idx], verbose=0)
    print(f"Resultado Fold {fold} - Accuracy: {scores[1]*100:.2f}%")
    cv_scores.append(scores[1] * 100)

# 6. RESULTADOS FINALES Y GUARDADO
print(f"\n" + "="*30)
print(f"[RESULTADO FINAL CV]: {np.mean(cv_scores):.2f}% (+/- {np.std(cv_scores):.2f}%)")
print("="*30)

print("\n" + "="*30)
print("RECORDATORIO DE MAPEO PARA FASTAPI:")
mapping = {0: "Refund", 1: "Technical", 2: "Cancellation", 3: "Product", 4: "Billing"}
for k, v in mapping.items():
    print(f"Neurona {k} -> {v}")
print("="*30)

# Guardado final
model.save('models/category_model.keras')
with open('models/tokenizer.pickle', 'wb') as h:
    pickle.dump(tokenizer, h)

print("\nProceso finalizado. Mapeo detectado: 0:Refund, 1:Tech, 2:Cancel, 3:Prod, 4:Bill")