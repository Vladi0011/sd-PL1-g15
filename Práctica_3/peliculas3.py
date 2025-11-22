import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd


proxy_url = "https://proxy-cache-func-jldiaz-e9b7ddh6graybmfr.italynorth-01.azurewebsites.net/api/proxy"
path_url = "/es/topgen.php"
url = f"{proxy_url}{path_url}"

resultadoWeb = requests.get(url)
soup = BeautifulSoup(resultadoWeb.text, "html.parser")

#En ocasiones una web puede restringir el scraping de su sitio web, puedes comprobar si has obtenido el HTML de la web consultada ejecutando el siguiente print:
# print(soup.prettify())

peliculasList = soup.find_all("div", class_="movie-card")
pelisPandas = []  # Lista a partir de la cual crearemos el DataFrame



for pelicula in peliculasList:
    titulo = pelicula.find("div", class_="mc-title")
    titulo = titulo.find("a").text
    año = pelicula.find("span", class_="mc-year").text

    pelisPandas.append({"Titulo": titulo, "Año": año})  # 1

pelis_df = pd.DataFrame(pelisPandas)  # 2

# Guardamos el DataFrame en archivos con diferentes formatos
pelis_df.to_csv('pelis.csv', index=True)
print('CSV creado correctamente')

pelis_df.to_json('pelis.json', orient='records')
print('JSON creado correctamente')

pelis_df.to_excel('pelis.xlsx', index=False)
print('Excel creado correctamente')