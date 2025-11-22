import requests
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urlparse  # ← línea añadida

proxy_url = "https://proxy-cache-func-jldiaz-e9b7ddh6graybmfr.italynorth-01.azurewebsites.net/api/proxy"
path_url = "/es/topgen.php"
url = f"{proxy_url}{path_url}"

resultadoWeb = requests.get(url)
soup = BeautifulSoup(resultadoWeb.text, "html.parser")

# print(soup.prettify())  # opcional

peliculasList = soup.find_all("div", class_="movie-card")

def obtener_puntuacion_a_la_fuerza(href):  #
    """
    Carga la ficha de la película a través del mismo proxy y
    devuelve la puntuación si está disponible.
    """
    try:
        # Convertir el href absoluto a solo el path para usar el prox
        p = urlparse(href) 
        detail_path = p.path if p.path else href 
        detail_url = f"{proxy_url}{detail_path}"  

        r = requests.get(detail_url) 
        dsoup = BeautifulSoup(r.text, "html.parser") 

        # Intentamos varios selectores habituales en la ficha
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
                txt = nodo.get_text(strip=True)
                # Normalizamos, quedándonos con algo tipo "8,7" o "8.7" 
                return txt.replace(',', '.')
        return None  
    except Exception:
        return None 

for pelicula in peliculasList:
    titulo_div = pelicula.find("div", class_="mc-title")
    enlace = titulo_div.find("a")
    titulo = enlace.text
    href = enlace.get("href") 

    año = pelicula.find("span", class_="mc-year").text

    # 1) Primero intentamos en el propio listado (por si acaso)
    puntuacion_node = pelicula.find("div", class_="mc-rating") 
    if puntuacion_node:  
        puntuacion = puntuacion_node.get_text(strip=True) 
    else:
        # 2) Si no está en el listado, vamos a la ficha 
        puntuacion = obtener_puntuacion_a_la_fuerza(href)

    if not puntuacion: 
        puntuacion = "Sin puntuación" 

    print(f"{titulo} ({año}) - Puntuación: {puntuacion}")

