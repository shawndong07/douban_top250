# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanTop250Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MovieItem(scrapy.Item):
    # 定义电影的属性
    name = scrapy.Field()
    year = scrapy.Field()
    image = scrapy.Field()
    image_path = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    rating = scrapy.Field()
    votes = scrapy.Field()


class MyItem(scrapy.Item):
    name = scrapy.Field()
    image_urls = scrapy.Field()
    # images = scrapy.Field()
    image_paths = scrapy.Field()
