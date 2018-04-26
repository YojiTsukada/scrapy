import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news' # spiderの名前

    # クロール対象とするドメインのリスト
    allowed_domains = ['news.yahoo.co.jp']

    # クロールを開始するURLのリスト。1要素のタプルの末尾にはカンマが必要。
    start_urls = ['http://news.yahoo.co.jp/']


    def parse(self, response):
        """
        トップページのトピックス一覧から個々のトピックスへのリンクを抜き出してたどる。
        """
        for url in response.css('ul.topics a::attr("href")').re(r'/pickup/\d+$'):
            yield scrapy.Request(response.urljoin(url), self.parse_topics)

    def parse_topics(self,response):
        pass
