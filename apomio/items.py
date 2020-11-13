# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def remove_n_strip(in_str):
    if type(in_str) != str:
        return in_str
    return in_str.replace("\n", "").strip()


def parse_rate(rate_str):
    rate = 0
    if len(rate_str) > 1:
        rate_str = rate_str[rate_str.rindex('/'):]
        if rate_str.find('1') > 0:
            rate = 1;
        elif rate_str.find('2') > 0:
            rate = 2;
        elif rate_str.find('3') > 0:
            rate = 3;
        elif rate_str.find('4') > 0:
            rate = 4;
        elif rate_str.find('5') > 0:
            rate = 5;
        if rate_str.find('half') > 0:
            rate += 0.5
    return rate


def parse_review(review_str):
    return int(review_str.replace('(', '').replace(')', ''))


def parse_price(price_str):
    return float(remove_n_strip(price_str).replace(u"\u20AC", '').replace(',', '.'))


def parse_total_price(gesamt_str):
    return parse_price(gesamt_str[gesamt_str.find("Gesamtkosten") + 12:])


class ApomioItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pzn = scrapy.Field(
        output_processor=TakeFirst()
    )
    product = scrapy.Field(
        input_processor=MapCompose(remove_n_strip),
        output_processor=TakeFirst()
    )
    provider = scrapy.Field(
        input_processor=MapCompose(remove_n_strip),
        output_processor=TakeFirst()
    )
    rate = scrapy.Field(
        input_processor=MapCompose(parse_rate),
        output_processor=TakeFirst()
    )
    reviews = scrapy.Field(
        input_processor=MapCompose(parse_review),
        output_processor=TakeFirst()
    )
    payment = scrapy.Field(
        input_processor=MapCompose(remove_n_strip),
        output_processor=TakeFirst()
    )
    delivery = scrapy.Field(
        input_processor=MapCompose(remove_n_strip),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(parse_price),
        output_processor=TakeFirst()
    )
    total_price = scrapy.Field(
        input_processor=MapCompose(parse_total_price),
        output_processor=TakeFirst()
    )
    # pass
