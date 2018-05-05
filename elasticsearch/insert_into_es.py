import sys
import hashlib
import json

from elasticsearch import Elasticsearch

# ElasticSearchのクライアントを作成する。第１引数でノードのリストを指定できる。
# defaultでは、localhost 9200ポートに接続するため省略可能。
es = Elasticsearch(['localhost:9200'])

# キーワード引数bodyでJSONに相当するdictを指定して、pagesインデックスを作成する。
# ignore = 400　は、インデックスが存在する場合でもエラーにしない。

result = es.indices.create(index='pages', ignore=400, body={
    # settingsという項目で、kuromoji_analyzer というアナライザーを定義する。
    # アナライザーは、転置インデックスの作成方法を指定するもの。
    "settings":{
        "analysis":{
            "analyzer":{
                "kuromoji_analyzer":{
                    # 日本語形態素解析を使って文字列を分割するkuromoji_tokenizerを使用。
                    "tokenizer":"kuromoji_tokenizer"
            }
        }
    }
},
# mappingsという項目で、pageタイプを定義する。
"mappings":{
    "page":{
        #_allは全てのフィールドを結合して、一つの文字列とした特殊なフィールド。
        # アナライザーとして、上で定義したkuromoji-_analyzerを使用。
        "_all":{"analyzer":"kuromoji_analyzer"},
        
        # url, title, content の3つのフィールドを定義。
        # title と content では、アナライザーとして上で定義したkuromoji_analyzerを使用。
        "properties":{
            "url":{"type":"string"},
            "title":{"type":"string","analyzer":"kuromoji_analyzer"},
            "content":{"type":"string","analyzer":"kuromoji_analyzer"}
           }
        }
    }
})

print(result) # EalsticSearchからのレスポンスを表示。

# コマンドライン引数の第１引数で指定したパスのファイルを読み込む
with open(sys.argv[1]) as f:
    for line in f:  # JSON Lines形式のファイルを1行ずつ読み込む。
        page = json.loads(line)# 行をJSONとしてパースする。
        # URLのSHA-1ハッシュ値をドキュメントのIDとする。
        # IDは、必須ではないが、設定しておくと同じIDが会った時に別のドキュメントが作成されるのではなく、
        # 同じドキュメントの新しいバージョンとなり、重複を避ける。
        doc_id = hashlib.sha1(page['url'].encode('utf-8')).hexdigest()
        # Elasticsearchにインデックス化（保存）する。
        result = es.index(index='pages',doc_type="page",id=doc_id,body=page)

        print(result) # ElasticSeachからのレスポンスを表示。


