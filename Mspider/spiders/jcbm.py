# -*- coding: utf-8 -*-
import json
import re
from urllib import parse

import scrapy
from scrapy import Request
from Mspider.items import JcmbspiderItem
from Mspider.utils.common import get_mdd5

class JcbmSpider(scrapy.Spider):
    name = 'jcbm'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        # url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract()

        post_nodes = response.css('#news_list .news_block')[:1]

        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")
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
            post_id = match_re.group(1)
            jcmb_item = JcmbspiderItem()
            title = response.css("#news_title a::text").extract_first("")
            # title = response.xpath("//*[@id='news_title']//a/text()").extract_first("")
            create_data = response.css("#news_info .time::text").extract_first("")
            match_re = re.match(".*?(\d+.*)", create_data)
            if match_re:
                create_data = match_re.group(1)
            # create_data = response.xpath("//*[@id=news_info]//*[@class=time]/text()").extract_first("")
            content = response.css("#news_content").extract()[0]
            tag_list = ",".join(response.css(".news_tags a::text").extract())
            # tag_list = ",".join(response.xpath("//*[@class='news_tags']//a/text()").extract())
            jcmb_item['title'] = title
            jcmb_item['url'] = response.url
            jcmb_item['create_data'] = create_data
            jcmb_item['content'] = content
            jcmb_item['tags'] = tag_list
            jcmb_item['front_image_url'] = [response.meta.get("image_url", "")]

            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),
                          meta={"jcmb_item": jcmb_item}, callback=self.parse_ajaxnums)

    def parse_ajaxnums(self, response):
        jcmb_item = response.meta.get("jcmb_item", "")
        j_data = json.loads(response.text)
        jcmb_item["praise_num"] = j_data["DiggCount"]
        jcmb_item["fav_nums"] = j_data["TotalView"]
        jcmb_item["comment_nums"] = j_data["CommentCount"]
        jcmb_item["url_object_id"] = get_mdd5(jcmb_item["url"])

        yield jcmb_item
