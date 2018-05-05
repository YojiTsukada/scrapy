# Scrapy

## Intall

$ pip install scrapy

$ scrapy startproject myproject


### Itemの作成
spider が抜き出したデータを格納しておくためのオブジェクト
- 複数の種類のデータを抜き出した時にクラスで判別できる
- あらかじめ定義したフィールドにしか代入できないため、フィールド名の間違いを回避できる
- 自分で新しいメソッドを定義できる


### Spiderの作成
$ scrapy genspider news news.yahoo.co.jp

### Spiderの実行
$ scrapy crawl news


### Scrapy Shell (Interactive Shell)
$ scrapy shell {1}


### For ElasticSearch
'''
$ brew install elasticseach
$ elasticsearch-plugin install analysis-kuromoji
$ pip install elasticsearch
'''