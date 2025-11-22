import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la página
url = "https://es.wikipedia.org/wiki/Anexo:Pa%C3%ADses_por_PIB_(nominal)"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

resultadoWeb = requests.get(url, headers=headers)
soup = BeautifulSoup(resultadoWeb.text, "html.parser")

# Localizamos las tablas de datos
tablas = soup.find_all("table", {"class": "wikitable"})
tabla = tablas[1]  # 0=FMI, 1=Banco Mundial, 2=World Factbook
# Creamos una lista donde almacenaremos los diccionarios con la información
paisesPandas = []  # Lista base para crear el DataFrame

# Recorremos las filas de la tabla, omitiendo la cabecera (<tr> inicial)
for fila in tabla.find_all("tr")[1:]:
    columnas = fila.find_all(["td", "th"])  # Busacmos las celdas de cada fila
    if len(columnas) >= 4:
        posicion = columnas[0].get_text(strip=True)
        variacion = columnas[1].get_text(strip=True)
        pais = columnas[2].get_text(strip=True)
        pib = columnas[3].get_text(strip=True)

        # Evitar filas raras (por si cuela alguna cabecera intermedia)
        if pais and pib:
            paisesPandas.append({
                "Posición": posicion,
                "Variación": variacion,
                "País": pais,
                "PIB (millones USD)": pib
            })

# Creamos un DataFrame de pandas con la lista de diccionarios
paises_df = pd.DataFrame(paisesPandas)

# Guardamos el DataFrame en archivos con diferentes formatos
paises_df.to_csv("paises_pib.csv", index=False)
print("CSV creado correctamente")

paises_df.to_excel("paises_pib.xlsx", index=False)
print("Excel creado correctamente")


