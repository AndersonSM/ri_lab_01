# -*- coding: utf-8 -*-
import scrapy
import json

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


    def extract_data(self, response):
        output = RiLab01Item()
        self.id += 1
        self.log('\n\n\n\nID: %s\n' % self.id)
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
        if (title is None or len(title) == 0):
            title = '?'

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
        if (desc is None or len(desc) == 0):
            desc = '?'

        # author
        author = response.xpath("//meta[@name='article:author']/@content")
        if len(author) > 0:
            author = author[0].extract()
        else:
            author = response.xpath("//meta[@property='og:site_name']/@content")
            if len(author) > 0:
                author = author[0].extract()
        self.log('AUTHOR: %s\n' % author)
        if (author is None or len(author) == 0):
            author = 'Gazeta do Povo'

        # date
        date = response.xpath("//meta[@property='article:published_time']/@content")
        if len(date) > 0:
            date = date[0].extract()
        else:
            date = response.xpath("//meta[@name='stats:pushedAt']/@content")
            if len(date) > 0:
                date = date[0].extract()
        self.log('DATE: %s\n\n\n\n' % date)
        if (date is None or len(date) == 0):
            date = '?'

        # section
        section = response.xpath("//meta[@name='gp:section']/@content")
        if len(section) > 0:
            section = section[0].extract()
        else:
            section = response.xpath("//meta[@name='article:section']/@content")
            if len(section) > 0:
                section = section[0].extract()
        self.log('SECTION: %s\n\n\n\n' % section)
        if (section is None or len(section) == 0):
            section = '?'

        output['_id'] = str(self.id)
        output['title'] = title
        output['sub_title'] = desc
        output['author'] = author
        output['date'] = date
        output['section'] = section
        output['url'] = response.url
        output['text'] = '?'

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