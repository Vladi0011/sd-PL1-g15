import scrapy

domain = "proxy-cache-func-jldiaz-e9b7ddh6graybmfr.italynorth-01.azurewebsites.net"
proxy_url = f"https://{domain}/api/proxy"
base_path = "/es/ranking.php?rn=ranking_fa_movies&page="

class FaSpiderMultipagina(scrapy.Spider):
    name = "fa_spider_multipagina"
    allowed_domains = [domain]
    start_urls = [f"{proxy_url}{base_path}1"]

    def parse(self, response):
        for pelicula in response.css("div.movie-card"):
            yield {
                "titulo": pelicula.css("div.mc-title a::text").get(),
                "año": pelicula.css("span.mc-year::text").get(),
                "tipo": pelicula.css("div.mc-title span::text").get(),
                "puntuacion": pelicula.css("div.avg-rating::text").get(),
                "director": pelicula.css("div.mc-director a::text").get()
            }

        # Avanzar a la siguiente página si existe
        siguiente = response.css("div.pagination a.next::attr(href)").get()
        if siguiente:
            siguiente_url = f"{proxy_url}{siguiente}"
            yield scrapy.Request(url=siguiente_url, callback=self.parse)
