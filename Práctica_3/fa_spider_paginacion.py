import scrapy

# Configuración del Proxy
domain = "proxy-cache-func-jldiaz-e9b7ddh6graybmfr.italynorth-01.azurewebsites.net"
proxy_url = f"https://{domain}/api/proxy"
# El path base
path_url = "/es/ranking.php?rn=ranking_fa_movies"

class FaSpiderPaginacion(scrapy.Spider):
    name = "fa_spider_paginacion"
    allowed_domains = [domain]
    # URL inicial
    start_urls = [f"{proxy_url}{path_url}"]

    def parse(self, response):
        # 1. Extraemos las películas de la página actual
        for pelicula in response.css("div.movie-card"):
            titulo = pelicula.css("div.mc-title a::text").get()
            ano = pelicula.css("span.mc-year::text").get()
            director = pelicula.css("div.mc-director a::text").get()
            
            # El número de posición es vital para pedir la siguiente página
            posicion = pelicula.css("div.position::text").get()

            yield {
                "Posicion": posicion,
                "Titulo": titulo,
                "Año": ano,
                "Director": director
            }

        # 2. Lógica de Paginación (El truco del POST explicado en el manual 4.3)
        
        # Obtenemos todos los números de posición de esta carga
        positions = response.css("div.position::text").getall()
        
        if positions:
            # Cogemos el último número (ej: 30, 60, 90...)
            last_number = positions[-1].strip()

            # FilmAffinity carga más pelis enviando un formulario a esta URL (sin el ?...)
            post_url = f"{proxy_url}/es/ranking.php"

            # Preparamos los datos que espera el servidor para darnos las siguientes 30
            formdata = {
                "from": last_number,             # Empezar desde la última que vimos
                "rankingId": "ranking_fa_movies", # El ID del ranking
                "count": "30",                   # Queremos 30 más
                "chv": "0"
            }

            # Si no hemos llegado a 150 películas (límite ejemplo), pedimos más
            if int(last_number) < 150:
                print(f"--- Solicitando más películas desde la {last_number} ---")
                yield scrapy.FormRequest(
                    url=post_url,
                    formdata=formdata,
                    callback=self.parse, # Volvemos a llamar a esta función con los nuevos datos
                    dont_filter=True     # Importante para que Scrapy no bloquee la URL repetida
                )

# COMANDO PARA EJECUTARLO (en terminal):
# scrapy runspider fa_spider_paginacion.py -O peliculas_paginadas.csv