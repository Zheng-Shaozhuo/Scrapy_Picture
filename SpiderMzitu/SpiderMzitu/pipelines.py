# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from SpiderMzitu.settings import DOWN_IMG_HOST
from SpiderMzitu.spiders.common import _strip, _execute


class SpidermzituPipeline(object):
    def process_item(self, item, spider):
        return item

class SpidermzituImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder_source = item['source']
        folder_strip = _strip(item['title'])
        try:
            image_name = str(request.url.split('/', 3)[-1]).replace('/', '_')
        except:
            image_name = time.time()
        folder_type = item['type']
        filename = u'images/{0}/{1}/{2}/{3}'.format(folder_source, folder_type, folder_strip, image_name)
        return filename

    def get_media_requests(self, item, info):
        # _host = DOWN_IMG_HOST[item['source']]
        for index in range(len(item['image_paths'])):
            img_path = item['image_paths'][index]
            # referer = item['urls'][index]
            yield scrapy.Request(img_path, meta={'item': item, 'accept': 'image/webp,image/apng,image/*,*/*;q=0.8'})
            # yield scrapy.Request(img_path, meta={'item': item, 'referer': referer,
            #                                      'accept': 'image/webp,image/apng,image/*,*/*;q=0.8', 'host': _host})

    def item_completed(self, results, item, info):
        ok_paths = []
        err_paths = []
        for i in range(0, len(results)):
            if results[i][0]:
                ok_paths.append(item['image_paths'][i])
            else:
                err_paths.append(item['image_paths'][i])
        # image_paths = [x['path'] for ok, x in results if ok]
        # download_image_paths = [x['url'] for ok, x in results if ok]
        # if not image_paths:
        #     raise DropItem("Item contains no images")

        if item['source'] == 'mm29':
            if len(ok_paths) > 0:
                _ok_paths = []
                for path in ok_paths:
                    _ok_paths.append(path + '/800.jpg')
                _execute("update mzitu_aitaotu_n set state = 1 where img_path in ('%s')" % ("','".join(_ok_paths)))
            if len(err_paths):
                _err_paths = []
                for path in err_paths:
                    _err_paths.append(path + '/800.jpg')
                _execute("update mzitu_aitaotu_n set state = 9 where img_path in ('%s')" % ("','".join(_err_paths)))
        else:
            if len(ok_paths) > 0:
                _execute("update mzitu_aitaotu_n set state = 1 where img_path in ('%s')" % ("','".join(ok_paths)))
            if len(err_paths) > 0:
                _execute("update mzitu_aitaotu_n set state = 9 where img_path in ('%s')" % ("','".join(err_paths)))
        return item