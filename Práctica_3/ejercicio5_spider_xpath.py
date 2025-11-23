import scrapy

class PibSpiderXpath(scrapy.Spider):
    name = "pib_spider_xpath"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://es.wikipedia.org/wiki/Anexo:Pa%C3%ADses_por_PIB_(nominal)"]

    def parse(self, response):
        # Busca la primera tabla con clase wikitable
        # XPath equivalente a css table.wikitable
        tabla = response.xpath('//table[contains(@class, "wikitable")]')[0]

        # Itera sobre los tr (filas), saltando la cabecera [position()>1]
        for fila in tabla.xpath('.//tr[position()>1]'):
            yield {
                # td[1] es la posición. text() saca el texto.
                "posicion": fila.xpath('./td[1]/text()').get(default="").strip(),
                
                # td[2] es el país, dentro hay un <a>
                "pais": fila.xpath('./td[2]//a/text()').get(),
                
                # td[3] es el PIB
                "pib_fmi": fila.xpath('./td[3]/text()').get(default="").strip(),
                
                # td[4] es el PIB Banco Mundial
                "pib_bm": fila.xpath('./td[4]/text()').get(default="").strip()
            }