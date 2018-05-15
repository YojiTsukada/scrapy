import re
import lxml.html
from pymongo import MongoClient

def scrape(key):
    """
    ワーカーで実行するタスク
    """

    # ローカルホストのMongoDBに接続する
    client = MongoClient('localhost',27017)

    # scrapingデータベースのebook_htmlsコレクションを得る。
    html_collection = client.scraping.ebook_htmls

    # MongoDBからkeyに該当するデータを探す。
    ebook_html = html_collection.find_one({'key':key})

    ebook = scrape_detail_page(key, ebook_html['url'], ebook_html['html'])

    # ebookコレクションを得る
    ebook_collection = client.scraping.ebooks

    # keyで高速に検索できるようにユニークなインデックスを作成する。
    ebook_collection.create_index('key', unique=True)
    # ebookを保存する。
    ebook_collection.insert_one(ebook)

def scrape_detail_page(key, url, html):
    """
    詳細ページのResponseから電子書籍の情報をdictで得る
    """

    root = lxml.html.fromstring(html)
    ebook = {
        'url': url, # URL
        'key': key, # URLから抜き出したキー
        'title': root.cssselect('#bookTitle')[0].text_content(),
        'price': root.cssselect('.buy')[0].text.strip(),
        'content': [normalize_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')],
    }

    return ebook

def normalize_spaces(s):
    """
    連続する空白を１つのスペースに置き換え、前後の空白は削除した新しい文字列を取得する
    """

    return re.sub(r'\s+','',s).strip()
    