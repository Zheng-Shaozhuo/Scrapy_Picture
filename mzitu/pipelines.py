# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import scrapy
import time
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MzituPipeline(object):
    def process_item(self, item, spider):
        return item

class MzituImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder_strip = item['name']
        image_guid = request.url.split('/')[-1]
        filename = u'images/{0}/{1}'.format(folder_strip, image_guid)
        return filename

    def get_media_requests(self, item, info):
        for img_url in item['image_urls']:
            referer = item['url']
            yield scrapy.Request(img_url, meta={'item': item, 'referer': referer,
                                                'accept' : 'image/webp,image/apng,image/*,*/*;q=0.8', 'host': 'i.meizitu.net'})

    def item_completed(self, results, item, info):
        if len(item['image_urls']) > 0:
            image_paths = [x['path'] for ok, x in results if ok]
            if not image_paths:
                raise DropItem("Item contains no images")
            return item


def strip(path):
    try:
        path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    except:
        path = int(time.time())
    return path