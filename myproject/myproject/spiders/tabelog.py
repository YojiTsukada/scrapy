from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractors import LinkExtractor

from myproject.items import Restaurant

class TabelogSpider(CrawlSpider):
    name = "tabelog"
    allowed_domains = ["tabelog.com"]
    start_urls = (
        # 東京ほ昼のランキングURL
        # 普通にWebサイトを見ていると、もっとパラメータが多くなるが、
        #　ページャーのリンクをみると、値が０のパラメータは省略できることがわかる。
        'https://tabelog.com/tokyo/rstLst/lunch/2/?LstCosT=2&RdoCosTp=1',
    )

    rules = [
        # ページャーをたどる（最大9ページ）
        # 正規表現の \d を \d+　に帰ると10ページ以降も辿れる
        Rule(LinkExtractor(allow=r'/\w+/rstLst/lunch/\d/')),

        # レストラン詳細ページをパースする。
        Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/$'),
            callback='parse_restaurant'),
    ]

    def parse_restaurant(self,response):
        """
        レストランの詳細ページをパースする。
        """
        # google Static Maps の画像の　URLから緯度と経度を取得。
        latitude, longitude = response.css(
            'img.js-map-lazyload::attr("data-original")').re(r'markers=.*?%7C([\d.]+),([\d.]+)'
            )

        #　キーの値を指定して、Restaurantオブジェクトを作成
        item = Restaurant(
            name = response.css('.display-name').xpath('string()').extract_first().strip(),
            address = response.css('[class="rstinfo-table__address"]').xpath('string()').extract_first().strip(),
            latitude = latitude,
            longitude = longitude,
            station = response.css('dt:contains("最寄り駅")+dd span::text').extract_first(),
            score = response.css('.rdheader-rating__score-val-dtl').xpath('string()').extract_first().strip(),
            review = response.css('[property="v:count"]').xpath('string()').extract_first().strip(),
            )

        yield item
