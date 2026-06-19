import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# ==========================
# Conexión a la página
# ==========================

url = "https://books.toscrape.com/"
response = requests.get(url)

print(f"Verificación del request: {response.status_code}")
# una salida 200 indica que el request fue exitoso

print(f"URL consultada: {response.url}")
print(f"Content-Type recibido: {response.headers.get('Content-Type')}")

# ==========================
# Parsear el HTML
# ==========================

soup = BeautifulSoup(response.text, "html.parser")

# Lista donde se almacenarán los datos
datos = []

# Menú de categorías
menu = soup.find("ul", class_="nav nav-list")

# Recorrer todas las categorías (excepto Books)
for categoria in menu.find_all("a")[1:]:

    href = categoria["href"]

    # Expresión regular para extraer el nombre de la categoría
    patron = re.search(r'category/books/(.*?)_\d+', href)

    if patron:
        nombre_categoria = patron.group(1)
        nombre_categoria = nombre_categoria.replace("-", " ").title()
    else:
        nombre_categoria = categoria.text.strip()

    # URL completa de la categoría
    url_categoria = url + href

    # Solicitar la página de la categoría
    response_categoria = requests.get(url_categoria)
    soup_categoria = BeautifulSoup(response_categoria.text, "html.parser")

    # Contar libros de la categoría
    frecuencia = len(
        soup_categoria.find_all("article", class_="product_pod")
    )

    # Guardar datos
    datos.append({
        "Categoria": nombre_categoria,
        "Frecuencia": frecuencia
    })

# ==========================
# Crear DataFrame
# ==========================

df_categorias = pd.DataFrame(datos)

print(df_categorias)

# Mostrar primeras filas
print("\nPrimeros registros:")
print(df_categorias.head())



