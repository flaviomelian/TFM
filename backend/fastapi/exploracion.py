import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

# 1. Cargar el dataset
df = pd.read_csv('dataset/cleaned_data.csv')
mapping = {0: "Refund", 1: "Technical", 2: "Cancellation", 3: "Product", 4: "Billing"}

# --- MANTENEMOS LOS PRINTS ---
print("--- Estructura del Dataset ---")
print(df.info())

print("\n--- Distribución de Categorías ---")
distribucion = df['category_label'].value_counts().rename(index=mapping)
print(distribucion)

df['text_len'] = df['full_text'].astype(str).apply(len)
print("\n--- Estadísticas de longitud de texto ---")
print(df['text_len'].describe())

# --- CONFIGURACIÓN DE PLOTS INICIALES (Barras e Histograma) ---
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(1, 2, figsize=(15, 6))

# Gráfico 1: Distribución de Clases
sns.barplot(x=distribucion.index, y=distribucion.values, ax=ax[0], hue=distribucion.index, palette="viridis", legend=False)
ax[0].set_title('Distribución de Categorías en el Dataset', fontsize=14, fontweight='bold')
ax[0].set_ylabel('Número de Muestras')
ax[0].set_xlabel('Categoría')

# Gráfico 2: Histograma de Longitud de Texto
sns.histplot(df['text_len'], bins=30, ax=ax[1], kde=True, color='teal')
ax[1].set_title('Histograma de Longitud de los Tickets', fontsize=14, fontweight='bold')
ax[1].set_xlabel('Longitud (caracteres)')
ax[1].set_ylabel('Frecuencia')

plt.tight_layout()
plt.savefig('visualizacion_estadistica.png') # Guardamos antes de mostrar
plt.show()

# --- NUEVA REPRESENTACIÓN: NUBE DE PALABRAS (WORDCLOUD) ---
print("\nGenerando Nube de Palabras bilingüe...")

# Combinamos stopwords de inglés y español para limpiar la nube
stopwords_es = ["el", "la", "de", "que", "un", "una", "en", "es", "por", "para", "con", "no", "mi", "me", "si"]
total_stopwords = set(list(STOPWORDS) + stopwords_es)

text_combined = " ".join(review for review in df.full_text.astype(str))

wordcloud = WordCloud(
    width=1000, 
    height=500, 
    background_color='white', 
    stopwords=total_stopwords,
    colormap='inferno',
    max_words=100
).generate(text_combined)

plt.figure(figsize=(15, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Nube de Palabras: Términos más frecuentes (Bilingüe)", fontsize=20, pad=20)

plt.savefig('wordcloud_dataset.png', dpi=300)
plt.show()

print("\nAnálisis completado. Gráficos guardados como 'visualizacion_estadistica.png' y 'wordcloud_dataset.png'.")