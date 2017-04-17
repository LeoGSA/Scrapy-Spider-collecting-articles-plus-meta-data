# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from sxtl.items import SxtlItem
from scrapy.http.request import Request


class SxtlSpider(Spider):
    name = "sxtl"

    start_urls = ['some-site']

    minimal_rating = 6 # the minimal rating of an article which we are interested in.

    def parse(self, response):
        """ Parses the article teasers. If article rating is more than minimal_rating, sends the article to futher scraping. """

        list_of_stories = response.xpath('//div[@id and @class="storyBox"]')

        stop = False

        for i in list_of_stories:

            pre_rating = i.xpath('div[@class="storyDetail"]/div[@class="storyDetailWrapper"]/div[@class="block rating_positive"]/span/text()').extract()
            rating = float(("".join(pre_rating)).replace("+", ""))

            link = "".join(i.xpath('div[@class="wrapSLT"]/div[@class="titleStory"]/a/@href').extract())

            if rating > minimal_rating:
                yield Request("".join(link), callback=self.parse_story)
            else:
                stop = True
                break

        # looking through other pages of article teasers
        if not stop:
            new_link = "".join(response.xpath('//a[@id="arr-nav-right-link"]/@href').extract())
            print('new_link', new_link)
            yield Request(new_link, callback=self.parse)


    def parse_story(self, response):
        """ Parses article text and article meta-data (author, publication date, name, categories, etc.) """

        item = SxtlItem()

        navig_panel = response.xpath('//div[@class="pNavig"]').extract()

        pre_rating = response.xpath('//span[@class="rating_positive"]/span/text()').extract()

        item['link'] = response.url
        item['rating'] = float(("".join(pre_rating)).replace("+", ""))
        item['name'] = "".join(response.xpath('//h1[@class="titleStory"]/text()').extract()).strip()
        item['date'] = "".join(response.xpath('//span[@class="date"]/text()').extract()).strip()
        item['categories'] = response.xpath('//div[@class="categories"]/a/span/text()').extract()
        item['parts'] = []
        item['author'] = "".join(response.xpath('//a[@class="author"]/text()').extract()).strip()
        item['text'] = response.xpath('//div[@id="storyText"]/div[@itemprop="description"]/descendant-or-self::node()/text()').extract()

        # checking whether the article has one or many pages. If one - exporting Item. If many - sending to scrape other pages.
        if navig_panel:
            t = u'Последняя'
            the_last_page = response.xpath('//a[text()="%s"]/@href' % t).extract()

            if the_last_page:
                item['last_page_link'] = "".join(response.xpath('//a[text()="%s"]/@href' % t).extract())
            else:
                item['last_page_link'] = "".join(response.xpath('//div[@class="pNavig"]/a[@href]/@href').extract()[-2])

            yield Request("".join(response.xpath('//a[@id="arr-nav-right-link"]/@href').extract()), meta={'item':item}, callback=self.get_text)
        else:
            yield item


    def get_text(self, response):
        """ Scraping other pages of a multy-page article. Exporting Item when done. """

        item = response.meta['item']

        item['text'].extend(response.xpath('//div[@id="storyText"]/div[@itemprop="description"]/descendant-or-self::node()/text()').extract())

        if response.url == item['last_page_link']:
            yield item
        else:
            yield Request("".join(response.xpath('//a[@id="arr-nav-right-link"]/@href').extract()), meta={'item':item}, callback=self.get_text)








