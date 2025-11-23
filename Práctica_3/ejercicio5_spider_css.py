import scrapy

class PibSpider(scrapy.Spider):
    name = "pib_spider"
    allowed_domains = ["wikipedia.org"]
    # Usamos la misma URL que en tu Ejercicio 3
    start_urls = ["https://es.wikipedia.org/wiki/Anexo:Pa%C3%ADses_por_PIB_(nominal)"]

    def parse(self, response):
        # Wikipedia tiene varias tablas, seleccionamos la primera que tenga la clase "wikitable"
        tabla = response.css('table.wikitable')[0]

        # Iteramos sobre las filas (tr), saltando la primera ([1:]) que es la cabecera
        for fila in tabla.css('tr')[1:]:
            # Extraemos los datos limpiando espacios y saltos de línea
            # Nota: En Wikipedia a veces el país es un enlace (a) y a veces texto, 
            # 'string' o 'text' suele funcionar para ambos.
            
            yield {
                # Característica 1: Ranking
                "posicion": fila.css("td:nth-child(1)::text").get(default="").strip(),
                
                # Característica 2: Nombre del País (buscamos el texto dentro del enlace <a> si existe)
                "pais": fila.css("td:nth-child(2) a::text").get(),
                
                # Característica 3: PIB (FMI)
                "pib_fmi": fila.css("td:nth-child(3)::text").get(default="").strip(),
                
                # Característica 4: Continente (o región, suele estar en la primera columna de la tabla oculta o visible)
                # Como alternativa simple, sacamos el PIB del Banco Mundial (columna 4)
                "pib_bm": fila.css("td:nth-child(4)::text").get(default="").strip()
            }

# COMANDO PARA EJECUTARLO (en terminal):
# scrapy runspider ejercicio5_spider.py -O paises_wiki.csv