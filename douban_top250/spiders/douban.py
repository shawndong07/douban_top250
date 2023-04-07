import scrapy

from douban_top250.items import MyItem


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

    def parse(self, response):
        # 提取电影信息
        for item in response.css('div.item'):
            myitem = MyItem()
            myitem['name'] = item.css('span.title::text').get()
            myitem['image_urls'] = [item.css('img::attr(src)').get()]

            yield myitem
        # # 提取下一页的URL
        # next_url = response.css('span.next>a::attr(href)').get()
        # if next_url:
        #     yield scrapy.Request(response.urljoin(next_url))

