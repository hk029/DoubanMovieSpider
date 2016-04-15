# -*- coding: utf-8 -*-
import scrapy
from doubanmovie.items import DoubanmovieItem
from scrapy.http import Request

class DoubantestSpider(scrapy.Spider):
    name = "doubantest"
    redis_key = 'doubantest:start_urls'
    #allowed_domains = ["douban.com/top250"]
    start_urls = (
        'http://movie.douban.com/top250/',
    )
    url = 'http://movie.douban.com/top250'

    def parse(self, response):
        # print response.body

        selector = scrapy.Selector(response)
        Movies = selector.xpath('//div[@class="info"]')
        for eachMovie in Movies:
            item = DoubanmovieItem()
            #get the title of each movie
            title = eachMovie.xpath('div[@class="hd"]/a')
            fulltitle = title.xpath('string(.)').extract()[0].replace('\n','').replace(' ','')
            print fulltitle
            #get the director of each movie
            info = eachMovie.xpath('div[@class="bd"]/p[@class=""]/text()').extract()[0].replace('\n','').replace(' ','')
            print info
            star = eachMovie.xpath('div[@class="bd"]/div/span[@class="rating_num"]/text()').extract()[0]
            print star
            quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote = '"'+quote[0]+'"'
            print quote
            item['title'] = fulltitle
            item['movieInfo'] = info
            item['star'] = star
            item['quote'] = quote
            yield item
        nextPage = selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextPage:
            nextPage = nextPage[0]
            print self.url+nextPage
            yield Request(self.url+nextPage,callback=self.parse)