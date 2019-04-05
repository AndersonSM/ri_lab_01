# -*- coding: utf-8 -*-
import scrapy
import json
import datetime

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class GazetaDoPovoSpider(scrapy.Spider):
    name = 'gazeta_do_povo'
    allowed_domains = ['gazetadopovo.com.br']
    start_urls = []
    pages_urls = []
    id = 0
    current_page = -1

    def __init__(self, *a, **kw):
        super(GazetaDoPovoSpider, self).__init__(*a, **kw)
        with open('./seeds/gazeta_do_povo.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())


    def get_tile(self, response):
        # title
        title = response.xpath("//meta[@property='og:title']/@content")
        if len(title) > 0:
            title = title[0].extract()
        else:
            title = response.xpath("//meta[@name='twitter:title']/@content")
            if len(title) > 0:
                title = title[0].extract()
            else:
                title = response.xpath("//meta[@name='gp:title']/@content")
                if len(title) > 0:
                    title = title[0].extract()
        self.log('TITLE: %s\n' % title)
        if title is None or len(title) == 0:
            title = '?'

        return title


    def get_desc(self, response):
        # desc
        desc = response.xpath("//meta[@property='og:description']/@content")
        if len(desc) > 0:
            desc = desc[0].extract()
        else:
            desc = response.xpath("//meta[@name='description']/@content")
            if len(desc) > 0:
                desc = desc[0].extract()
            else:
                desc = response.xpath("//meta[@name='twitter:description']/@content")
                if len(desc) > 0:
                    desc = desc[0].extract()
                else:
                    desc = response.xpath("//meta[@property='cXenseParse:gdp-expiration']/@content")
                    if len(desc) > 0:
                        desc = desc[0].extract()
        self.log('DESC: %s\n' % desc)
        if desc is None or len(desc) == 0:
            desc = '?'

        return desc


    def get_author(self, response):
        # author
        author = response.xpath("//meta[@name='article:author']/@content")
        if len(author) > 0:
            author = author[0].extract()
        else:
            author = response.xpath("//meta[@property='og:site_name']/@content")
            if len(author) > 0:
                author = author[0].extract()
        self.log('AUTHOR: %s\n' % author)
        if author is None or len(author) == 0:
            author = 'Gazeta do Povo'

        return author


    def get_date(self, response):
        # date
        date = response.xpath("//meta[@property='article:published_time']/@content")
        if len(date) > 0:
            date = date[0].extract()
        else:
            date = response.xpath("//meta[@name='stats:pushedAt']/@content")
            if len(date) > 0:
                date = date[0].extract()
        self.log('DATE: %s\n\n\n\n' % date)
        if date is None or len(date) == 0:
            date = '?'
        else:
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
            date = date_obj.strftime("%d/%m/%Y %H:%M:%S")

        return date


    def get_section(self, response):
        # section
        section = response.xpath("//meta[@name='gp:section']/@content")
        if len(section) > 0:
            section = section[0].extract()
        else:
            section = response.xpath("//meta[@name='article:section']/@content")
            if len(section) > 0:
                section = section[0].extract()
        self.log('SECTION: %s\n\n\n\n' % section)
        if section is None or len(section) == 0:
            section = '?'

        return section


    def get_text(self, response):
        # text
        text = ''.join(response.css('.paywall-google ::text').extract())
        if len(text) == 0:
            text = ''.join(response.css('.news-text ::text').extract())
        if len(text) == 0:
            text = ''.join(response.css('.texto-post ::text').extract())
        self.log('TEXT: %s\n\n\n\n' % text)
        if text is None or len(text) == 0:
            text = '?'

        return text


    def extract_data(self, response):
        output = RiLab01Item()
        self.id += 1
        self.log('\n\n\n\nID: %s\n' % self.id)

        output['_id'] = str(self.id)
        output['title'] = self.get_tile(response)
        output['sub_title'] = self.get_desc(response)
        output['author'] = self.get_author(response)
        output['date'] = self.get_date(response)
        output['section'] = self.get_section(response)
        output['text'] = self.get_text(response)
        output['url'] = response.url

        yield output


    def get_articles(self, response):
        if len(self.pages_urls) == 0:
            self.pages_urls = response.css('.c-paginacao ul li a::attr(href)').getall()[1:10]

        for url in response.css('.c-chamada a::attr(href)').getall():
            yield response.follow(response.urljoin(url), callback=self.extract_data)

        self.current_page += 1
        yield response.follow(response.urljoin(self.pages_urls[self.current_page]), callback=self.get_articles)


    def parse(self, response):
        yield response.follow(response.urljoin(response.css('a.ultimas::attr(href)').get()), callback=self.get_articles)