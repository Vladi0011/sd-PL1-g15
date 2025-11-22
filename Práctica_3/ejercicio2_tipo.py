import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

proxy_url = "https://proxy-cache-func-jldiaz-e9b7ddh6graybmfr.italynorth-01.azurewebsites.net/api/proxy"
path_url = "/es/topgen.php"
url = f"{proxy_url}{path_url}"

resultadoWeb = requests.get(url)
soup = BeautifulSoup(resultadoWeb.text, "html.parser")

peliculasList = soup.find_all("div", class_="movie-card")

def obtener_puntuacion_a_la_fuerza(href):
    """
    Carga la ficha a través del proxy y devuelve la puntuación si está.
    """
    try:
        p = urlparse(href)
        detail_path = p.path if p.path else href
        detail_url = f"{proxy_url}{detail_path}"

        r = requests.get(detail_url)
        dsoup = BeautifulSoup(r.text, "html.parser")

        candidatos = [
            ('span', {'itemprop': 'ratingValue'}),
            ('div', {'id': 'movie-rat-avg'}),
            ('div', {'class': 'avg-rating'}),
            ('span', {'class': 'avg-rating'}),
            ('div', {'class': 'rating'}),
            ('span', {'class': 'rating'}),
        ]
        for tag, attrs in candidatos:
            nodo = dsoup.find(tag, attrs=attrs)
            if nodo:
                return nodo.get_text(strip=True).replace(',', '.')
        return None
    except Exception:
        return None

def es_serie_o_miniserie(href): # función para detectar serie/miniserie
    try:
        p = urlparse(href)
        detail_path = p.path if p.path else href
        detail_url = f"{proxy_url}{detail_path}"

        r = requests.get(detail_url)
        dsoup = BeautifulSoup(r.text, "html.parser") 

        texto = dsoup.get_text(" ", strip=True).lower()
        # Palabras clave habituales en fichas de series/miniseries
        claves = ["serie de tv", "miniserie", "temporadas", "episodios"]
        return any(c in texto for c in claves)  #
    except Exception:
        return False  #

for pelicula in peliculasList:
    titulo_div = pelicula.find("div", class_="mc-title")
    enlace = titulo_div.find("a")
    titulo = enlace.text
    href = enlace.get("href")

    año = pelicula.find("span", class_="mc-year").text

    #PRIMERO puntuación en listado; si no, en ficha (como en Ej.1)
    puntuacion_node = pelicula.find("div", class_="mc-rating")
    if puntuacion_node:
        puntuacion = puntuacion_node.get_text(strip=True)
    else:
        puntuacion = obtener_puntuacion_a_la_fuerza(href)

    if not puntuacion:
        puntuacion = "Sin puntuación"

    #prefijo de tipo consultando la ficha (el listado no trae el badge)
    prefijo = "[S]" if es_serie_o_miniserie(href) else "[P]"

    print(f"{prefijo} {titulo} ({año}) - Puntuación: {puntuacion}")
