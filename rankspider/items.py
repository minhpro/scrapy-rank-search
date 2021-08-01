# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RankItem(scrapy.Item):
    id = scrapy.Field()
    error = scrapy.Field()
    rank = scrapy.Field()
    url = scrapy.Field()
