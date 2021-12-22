import scrapy
import json


class LeroymerlinDecorSpider(scrapy.Spider):
    name = 'leroymerlin_decor'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/dekor/?page=1']
    custom_settings = {'FEED_URI': "leroymerlin_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING' : 'utf-8'}
    flag = 0
    id = 0

    def parse(self, response):
        print("procesing:" + response.url)
        # Извлечение данных с помощью селекторов CSS
        product_name = response.css('.t9jup0e_plp.p1h8lbu4_plp::text').extract()

        price_range = response.css('.t3y6ha_plp.xc1n09g_plp.p1q9hgmc_plp::text').extract()
        for i in range(0, len(price_range)):
            price_range[i] = price_range[i].replace('\xa0', '')
        row_data = zip(product_name, price_range)


        # извлечение данных строки
        for item in row_data:
            scraped_info = {
                # 'id': self.id,
                'page': response.url,
                'product_name': item[0],
                'price_range': item[1],
            }
            yield scraped_info
        next_page = (response.css('.bex6mjh_plp.s15wh9uj_plp.l7pdtbg_plp.r1yi03lb_plp.sj1tk7s_plp::attr(href)').extract())[-1]

        print('ФЛАГ', (self.flag), type(next_page), next_page)
        if next_page and self.flag < 300:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse)
                self.flag += 1

# scrapy crawl leroymerlin_decor


