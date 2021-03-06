from elasticsearch import Elasticsearch
from bottle import route, run, request, template

import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

es = Elasticsearch(['localhost:9200'])

@route('/')
def index():
    """
    / へのリクエストを処理する。
    """

    # クエリ(?q=の値)を取得する。
    query = request.query.q
    
    # クエリがある場合は検索結果を、ない場合は、[]をpagesに代入する。
    pages = search_pages(query) if query else []

    # Bottleのテンプレート機能を使って、search.tpl というファイルから読み込んだテンプレートに
    # query と pages の値を渡して、レンダリングした結果をレスポンスボディとして返す。
    #return template('search', query=query, pages=pages)
    return template('search', query=query, pages=pages)

def search_pages(query):
    """
    引数のクエリでElasticSearchからWebページを検索し、結果のリストを返す。
    """

    # SimpleQueryStingを使って、検索する。
    # contentフィールドでマッチする部分をハイライトするよう設定している。
    
    result = es.search(index='pages', doc_type='page', body={
        "query":{
            "simple_query_string":{
                "query":query,
                "fields":["title^5","content"],
                "default_operator":"and"
            }
        },
        "highlight":{
            "fields":{
                "content":{
                    "fragment_size":150,
                    "number_of_fragments":1,
                    "no_match_size":150
                }
            }
        }

    })
    return result['hits']['hits']

if __name__ == "__main__":
    # 開発用のHTTPサーバを起動する。
    run(host="0.0.0.0", port=8000,debug=True, reloader=True)