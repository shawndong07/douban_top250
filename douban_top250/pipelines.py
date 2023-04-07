# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter, JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline


class DoubanTop250Pipeline:
    def process_item(self, item, spider):
        return item


# 定义一个Pipeline类，将Item对象存储为JSON文件
class JsonWriterPipeline:
    def __init__(self):
        self.file = open('items.jl', 'wb')
        self.exporter = JsonLinesItemExporter(self.file, ensure_ascii=False, indent=4)

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class JsonPipeline:
    def __init__(self):
        self.file = open('items.json', 'wb')
        self.exporter = JsonItemExporter(self.file, ensure_ascii=False, indent=4)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        print(f'item: {item}')
        self.exporter.export_item(item)
        return item


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return request.url.split('/')[-1]

    def item_completed(self, results, item, info):
        print(f'item: {item} result: {results}')
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['image_paths'] = image_paths
        return item

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)
