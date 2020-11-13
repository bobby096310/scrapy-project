import scrapy
from scrapy.loader import ItemLoader
from apomio.items import ApomioItem

class ApomioSpider(scrapy.Spider):
    name = "apomio"
    productXPZN = {}
    def start_requests(self):
        urlstem = 'https://www.apomio.de/suche?query='
        pzns = [
            '171865',
            '1587486',
            '4637585',
            '4002065',
            '2483072',
            '10793390',
            '2200186',
            '12645883',
            '13780867',
            '13839425'
        ]
        for PZN in pzns:
            yield scrapy.Request(url=urlstem + PZN, callback=self.parse, meta={'pzn':PZN})

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = f'quotes-{page}.html'
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)exi
    #     self.log(f'Saved file {filename}')

    def parse(self, response):
        pzn = response.meta['pzn']
        if 'product' in response.meta:
            product = response.meta['product']
        else:
            product = self.parseString(response.css("div.overflow-x-scroll li::text")[-1].get())

        for cp_row in response.css('div.comparison-row'):
            loader = ItemLoader(item=ApomioItem(), selector=cp_row)
            loader.add_value('pzn', pzn)
            loader.add_value('product', product)
            loader.add_css('provider', 'span.w-5\/6::text')
            loader.add_value('rate', cp_row.css('div.rating img').xpath('@src').get())
            loader.add_css('reviews', 'div.rating span.text-xxs::text')
            loader.add_value('payment', cp_row.css("span.mb-3::text")[0].get())
            if len(cp_row.css("span.mb-3::text")) > 1:
                loader.add_value('delivery', cp_row.css("span.mb-3::text")[1].get())
            else:
                loader.add_value('delivery', '')
            loader.add_css('price', 'a.text-red::text')
            loader.add_value('total_price', cp_row.css('div.text-right span.text-xs::text')[-1].get())
            yield loader.load_item()
        showmore = 'https://www.apomio.de/preisvergleich-zeige-alle-angebote/'
        yield response.follow(url=showmore + pzn, callback=self.parse, meta={'pzn': pzn, 'product':product})

    def parseString(self, in_str):
        if type(in_str) != str:
            return in_str
        return in_str.replace("\n","").strip()