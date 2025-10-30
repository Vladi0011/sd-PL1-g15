import requests
from requests import get
from bs4 import BeautifulSoup

proxy_url = "https://proxy-cache-func-jldiaz-e9b7ddh6graybmfr.italynorth-01.azurewebsites.net/api/proxy"
path_url = "/es/topgen.php"
url = f"{proxy_url}{path_url}"

resultadoWeb = requests.get(url)
soup = BeautifulSoup(resultadoWeb.text, "html.parser")

print(soup.prettify()) # 1

peliculasList = soup.find_all("div", class_="movie-card")

for pelicula in peliculasList:
    print(pelicula, end="\n")
