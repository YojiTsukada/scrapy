# Scrapy


$ scrapy startproject myproject


### Itemの作成
spider が抜き出したデータを格納しておくためのオブジェクト
- 複数の種類のデータを抜き出した時にクラスで判別できる
- あらかじめ定義したフィールドにしか代入できないため、フィールド名の間違いを回避できる
- 自分で新しいメソッドを定義できる


### Spiderの作成
$ scrapy genspider news news.yahoo.co.jp
