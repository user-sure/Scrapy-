import scrapy
from spider2026.items import MovieItem
from scrapy import Request

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
        "Cookie":'__utmc=223695111;__utmz=30149280.1782637166.5.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/;_pk_id.100001.4cf6=18cbebb015083a46.1781608646.;bid=pWW0aDF7NbE;ck=ahS8;__utmb=223695111.0.10.1782637166;__utma=30149280.1711455584.1781608646.1782635134.1782637166.5;_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1782635134%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D;__utmb=30149280.0.10.1782637166;__utmc=30149280;__utma=223695111.488239336.1781608646.1782635134.1782637166.5;__utmz=223695111.1782637166.5.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/;__yadk_uid=Pd85CMDMuU7gHWwsotUAZJN00L9pE7p5;_pk_ses.100001.4cf6=1;_vwo_uuid_v2=DA2453CAA47834592BB430CDBFDBCA695|614dafe87d76f43587d21183f88f7dc4;ap_v=0,6.0;dbcl2="295830516:BCsB9ubinOI";ll="118230";push_doumail_num=0;push_noty_num=0'
    }
    def start_requests(self):
        for page in range(10):
            start = page * 25
            yield Request(url=f'https://movie.douban.com/top250?start={start}&filter=',headers=self.headers)

    def parse(self, response):
        list_items = response.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            movie_item = MovieItem()
            # or 兜底，取不到值填充文字，避免None报错
            movie_item['title'] = list_item.css('span.title::text').extract_first() or '无片名'
            # 修复评分class：rating_num → rating
            movie_item['rank'] = list_item.css('span.rating_num::text').extract_first() or '无评分'
            movie_item['subject'] = list_item.css('p.quote > span::text').extract_first() or '无短评'
            yield movie_item