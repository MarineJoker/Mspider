# -*- coding: utf-8 -*-
import json
from urllib import parse

import scrapy
import re
from scrapy import Request


class JcbmSpider(scrapy.Spider):
    name = 'jcbm'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        # url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract()

        post_nodes = response.css('#news_list .news_block')[:1]

        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(href)').extract_first("")
            post_url = post_node.css('h2 a::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"image_url": image_url}, callback=self.parse_detail)

        # next_url = response.css("div.pager a:last-child::text").extract_first("")
        next_url = response.xpath("//div[@class='pager']//a[contains(text(),'Next >')]/@href").extract_first("")
        if next_url != "":
            # next_url = response.css("div.pager a:last-child::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            title = response.css("#news_title a::text").extract_first("")
            # title = response.xpath("//*[@id='news_title']//a/text()").extract_first("")

            create_data = response.css("#news_info .time::text").extract_first("")
            # create_data = response.xpath("//*[@id=news_info]//*[@class=time]/text()").extract_first("")
            content = response.css("#news_content").extract()[0]
            tag_list = ",".join(response.css(".news_tags a::text").extract())
            # tag_list = ",".join(response.xpath("//*[@class='news_tags']//a/text()").extract())
            post_id = match_re.group(1)

            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)), callback=self.parse_nums)
        # /html/body/div[2]/div[2]/div[3]/div[1]/div[2]/h2/a/@herf
        # // *[ @ id = "entry_662086"] / div[2] / h2 / a
        # //div[@id="new_list"]//h2[@class=new_entry]/a/@href

    def parse_ajaxnums(self, response):
        j_data = json.loads(response.text)
        praise_nums = j_data["DiggCount"]
        fav_nums = j_data["totalView"]
        comment_nums = j_data["CommentCount"]
