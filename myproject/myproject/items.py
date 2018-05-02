# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Headline(scrapy.Item):
    """
    ニュースのヘッドラインを表すItem
    """

    title = scrapy.Field()
    body = scrapy.Field()

item = Headline()
item['title'] = 'Example'
print(item['title']) # Exampleと表示される。



class Restaurant(scrapy.Item):
    """
    食べログのレストラン情報
    """

    name = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    station = scrapy.Field()
    score = scrapy.Field()
    review = scrapy.Field()
