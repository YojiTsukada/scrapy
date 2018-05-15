import time
import re
import sys

import requests
import lxml.html

from pymongo import MongoClient
from redis import Redis
from rq import Queue


def main():
    """
    クローラーのメイン処理
    """

    q = Queue(connection=Redis())

    # ローカルホストのMongoDBに接続
    client = MongoClient('localhost', 27017)
    
    # scrapingデータベースのebooK_htmlコレクションを得る。
    collection = client.scraping.ebook_htmls

    # keyで高速に検索できるように、ユニークなインデックスを作成する。
    collection.create_index('key',unique=True)

    session = requests.Session()
    
    # 一覧ページを取得する
    response = session.get('http://gihyo.jp/dp')

    # 詳細ページのURL一覧を得る。
    urls = scrape_list_page(response)

    for url in urls:
        # url からキーを取得する。
        key = extract_key(url)

        # Mongoからkeyに該当するデータを探す。
        ebook_html = collection.find_one({'key':key})

        # MongDBに存在しない場合だけ、詳細ページをクロールする
        if not ebook_html:
            time.sleep(1)
            print('Fetching {0}'.format(url), file=sys.stderr)
            # 詳細ページを取得する。
            response = session.get(url)

            # HTMLをMongoDBに保存する
            collection.insert_one({
                'url':url,
                'key':key,
                'html':response.content,
            })

            # キューにジョブを追加する。
            # result_ttl = 0 という引数はタスクの戻り値を保存しないことを意味する。
            q.enqueue("tasks.scrape", key, result_ttl=0)

def scrape_list_page(response):
    """
    一覧ページの Responseから詳細ページのURLを抜き出す。
    """

    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)

    for a in root.cssselect('#listBook a[itemprop="url"]'):
        url = a.get('href')
        yield url


def extract_key(url):
    """
    URLからキー（URLの末尾のISBN)を抜き出す
    """

    m = re.search(r'/([^/]+)$', url)
    return m.group(1)

if __name__ == '__main__':
    main()
    