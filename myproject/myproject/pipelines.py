# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MyprojectPipeline(object):
    def process_item(self, item, spider):
        return item


from scrapy.exceptions import DropItem

class ValidationPipeline(object):
    """
    Itemを検証するPipeline
    """

    def process_item(self, item, spider):
        if not item['title']:
            # titleフィールドが取得できていない場合は、破棄する。
            # DropItem()の引数は破棄する理由を表すメッセージ
            raise DropItem('Missing title')


        return item # titleフィールドが正しく取得できている場合
