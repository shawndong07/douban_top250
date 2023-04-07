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

    # def save_image(self, response):
    #     # 从meta中获取item对象
    #     print(f'response ===================: {response}')
    #     item = response.meta['item']
    #     # 将图片保存到本地目录中
    #     image_path = item['image_path']
    #     with open(image_path, 'wb') as f:
    #         # 使用urllib库实现流式写入
    #         with urllib.request.urlopen(item['image_url']) as response_stream:
    #             for chunk in response_stream:
    #                 f.write(chunk)
