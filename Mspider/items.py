# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JcmbspiderItem(scrapy.Item):
    title = scrapy.Field()
    create_data = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_path = scrapy.Field()
    front_image_url = scrapy.Field()
    praise_num = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()