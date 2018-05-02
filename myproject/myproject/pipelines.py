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



from pymongo import MongoClient


class MongoPipeline(object):
    """
    ItemをMongoDBに保存するPipeline
    """

    def open_spider(self,spider):
        """
        Spiderの開始時にMongoDBに保存する
        """

        # ホストとポートを指定して、クライアントを作成
        self.client = MongoClient('localhost',27017)

        # scraping-book データベースを取得
        self.db = self.client['tabelog']

        # itemsコレクションを取得
        self.collection = self.db['shops']


    def close_spider(self, spider):
        """
        Spiderの終了時にMongoDBへの接続を切断する
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        Itemをコレクションに追加する
        """

        # insert_one()の引数は書き換えられるので、コピーしたdictを渡す。
        self.collection.insert_one(dict(item))

        return item
