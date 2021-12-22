import scrapy
import json


class LeroymerlinDecorSpider(scrapy.Spider):
    name = 'leroymerlin_decor'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/dekor/?page=918']
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
        # Извлечение данных с использованием xpathscrapy crawl leroymerlin_decor
        # orders = response.xpath("//em[@title='Total Orders']/text()").extract()
        # company_name = response.xpath("//a[@class='store $p4pLog']/text()").extract()

        row_data = zip(product_name, price_range)


        # извлечение данных строки
        for item in row_data:
            # создать словарь для хранения извлеченной информации

            scraped_info = {
                # 'id': self.id,
                'page': response.url,
                'product_name': item[0],
                # item[0] означает продукт в списке и т. д., индекс указывает, какое значение назначить
                'price_range': item[1],
                # 'orders': item[2],
                # 'company_name': item[3],
            }
            yield scraped_info
            # self.id+=1
        # next_page = response.css('.bex6mjh_plp.o1ojzgcq_plp.l7pdtbg_plp.r1yi03lb_plp.sj1tk7s_plp::attr(href)').get()
        # if next_page != None and self.flag < 3:
        #     yield scrapy.Request(
        #         response.urljoin(next_page),
        #         callback=self.parse)
        #     self.flag += 1

        # NEXT_PAGE_SELECTOR = 'a.bex6mjh_plp.s15wh9uj_plp.l7pdtbg_plp.r1yi03lb_plp.sj1tk7s_plp::attr(href)'


        # class ="bex6mjh_plp s15wh9uj_plp l7pdtbg_plp r1yi03lb_plp sj1tk7s_plp"

        next_page = (response.css('.bex6mjh_plp.s15wh9uj_plp.l7pdtbg_plp.r1yi03lb_plp.sj1tk7s_plp::attr(href)').extract())[-1]

        print('ФЛАГ', (self.flag), type(next_page), next_page)
        if next_page and self.flag < 300:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse)
                self.flag += 1

          # yield response.follow(next_page,callback=self.parse)



            # генерируем очищенную информацию для скрапа
            # yield scraped_info
# scrapy crawl leroymerlin_decor

# bex6mjh_plp.o1ojzgcq_plp.l7pdtbg_plp.r1yi03lb_plp.sj1tk7s_plp
