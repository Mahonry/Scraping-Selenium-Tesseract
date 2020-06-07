import scrapy
from scrapy.crawler import CrawlerProcess


class spider12(scrapy.Spider): #Spider es el scrapper generico de scrapy
    name = 'spider12'
    allowed_domains = ['pagina12.com.ar']
    
    custom_settings = {'FEED_FORMAT':'json',
                      'FEED_URI':'resultados.json',
                      'DEPTH_LIMIT':2,
                      'FEED_EXPORT_ENCODING': 'utf-8'}
    
    start_urls = ['https://www.pagina12.com.ar/secciones/el-pais',
                 'https://www.pagina12.com.ar/secciones/economia',
                 'https://www.pagina12.com.ar/secciones/sociedad',
                 'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
                 'https://www.pagina12.com.ar/secciones/el-mundo',
                 'https://www.pagina12.com.ar/secciones/deportes',
                 'https://www.pagina12.com.ar/secciones/contratapa']
                 #'https://www.pagina12.com.ar/secciones/audiovisuales']
    
    def parse(self, response):
        # Articulo Promocionado
        nota_promocionada = response.xpath('//div[@class="featured-article__container"]/a/@href').get()
        
        if nota_promocionada is not None:
            yield response.follow(nota_promocionada, callback = self.parse_nota) 
        
        #Listado de notas
        notas = response.xpath('//ul[@class="article-list"]//li//h2//a/@href').getall()
        for nota in notas:
            yield response.follow(nota, callback = self.parse_nota)
        
        #Link a la siguiente pagina
        next_page = response.xpath('//a[@class="pagination-btn-next"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
            
    def parse_nota(self, response):
        #Extraccion del titulo de la nota
        titulo = response.xpath('//div[@class="article-titles"]/h1[@class="article-title"]/text()').get()
        
        #Extraccion de la fecha de la nota
        fecha = response.xpath('//span[@pubdate="pubdate"]/@datetime').get()
        
        #Extraccion de la volanta de la nota
        volanta = response.xpath('//h2[@class="article-prefix"]/text()').get()
        
        #Extraccion del cuerpo de la nota
        cuerpo = ''.join(response.xpath('//div[@class="article-text"]/p/text()').getall())
        
        #Extraccion del autor de la nota 
        autor = response.xpath('//div[@class="article-author"]/a/text()').get()
        
        yield {'url':response.url,
              'titulo':titulo,
              'fecha':fecha,
              'volanta':volanta,
              'cuerpo':cuerpo,
              'autor':autor}

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(spider12)
    process.start()