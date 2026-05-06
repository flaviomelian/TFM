import pandas as pd

# Cargamos tu CSV
df = pd.read_csv('dataset/cleaned_data.csv')

print("--- INVESTIGACIÓN DE CATEGORÍAS ---")
for i in range(5):
    print(f"\n>>> ¿QUÉ ES LA CATEGORÍA {i}?")
    # Sacamos los primeros 5 ejemplos de esa etiqueta
    ejemplos = df[df['category_label'] == i]['full_text'].head(5).values
    for j, texto in enumerate(ejemplos, 1):
        print(f"  {j}. {texto[:100]}...") # Imprime los primeros 100 caracteres