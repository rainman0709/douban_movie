import scrapy
from douban.items import DoubanItem

class doubanSpider(scrapy.Spider):
    name = "douban_movie"
    start_urls = []
    for i in range(1888,2017):
        start_urls.append('https://movie.douban.com/tag/' + str(i))

    def parse(self, response):
        sites = response.xpath('//div[@class="article"]/div[2]/table')
        for site in sites:
            item = DoubanItem()

            movie_year = response.xpath('//head/title/text()').extract()
            item['movie_year'] = movie_year[0].strip().encode('utf-8') if len(movie_year) > 0 else ''
            address = site.xpath('tr/td[2]/div/a/@href').extract()
            item['address'] = address[0].strip().encode('utf-8') if len(address) > 0 else ''
            movie_name = site.xpath('tr/td[2]/div/a/text()').extract()
            item['movie_name'] = movie_name[0].strip().encode('utf-8') if len(movie_name) > 0 else ''
            movie_describe = site.xpath('tr/td[2]/div/p/text()').extract()
            item['movie_describe'] = movie_describe[0].strip().encode('utf-8') if len(movie_describe) > 0 else ''
            score = site.xpath('tr/td[2]/div/div/span[2]/text()').extract()
            item['score'] = score[0].strip().encode('utf-8') if len(score) > 0 else ''
            judge_number = site.xpath('tr/td[2]/div/div/span[3]/text()').extract()
            item['judge_number'] = judge_number[0].strip().encode('utf-8') if len(judge_number) > 0 else ''

            yield item

        next = response.xpath('//*[@id="content"]/div/div[1]/div[3]/span[@class="next"]/a/@href').extract()
        next_page = next[0] if len(next) > 0 else None
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield  scrapy.Request(next_page, callback=self.parse)