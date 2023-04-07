import scrapy
from scrapy.loader import ItemLoader

from douban_top250.items import MyItem, MovieItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'douban_top250.pipelines.ImagePipeline': 1,
            'douban_top250.pipelines.JsonPipeline': 100,
        },
        'IMAGES_STORE': 'images'
    }

    def parse(self, response, **kwargs):

        # 解析电影列表，获取电影详情页链接
        movie_links = response.css('div.hd a::attr(href)').getall()

        # 遍历电影详情页链接，发送HTTP请求，获取电影详情信息
        for link in movie_links:
            yield scrapy.Request(url=link, callback=self.parse_movie)

        # # 解析下一页链接，继续爬取
        # next_page_link = response.css('span.next a::attr(href)').get()
        # if next_page_link:
        #     next_page_link = f'{self.start_urls[0]}{next_page_link}'
        #     yield scrapy.Request(url=next_page_link, callback=self.parse)

    @staticmethod
    def parse_movie(response):
        # 创建ItemLoader，用于填充MovieItem
        loader = ItemLoader(item=MovieItem(), response=response)

        # 解析电影详情页内容，获取需要的数据
        loader.add_css('name', 'h1 span[property="v:itemreviewed"]::text')
        loader.add_css('year', 'h1 span.year::text', re=r'\((.*)\)')
        loader.add_css('image_urls', 'a.nbgnbg img::attr(src)')
        loader.add_css('director', 'a[rel="v:directedBy"]::text')
        loader.add_css('actors', 'a[rel="v:starring"]::text')
        loader.add_css('rating', 'strong.rating_num::text')
        loader.add_css('votes', 'span[property="v:votes"]::text')

        # 返回填充好的Item
        item = loader.load_item()

        return item
