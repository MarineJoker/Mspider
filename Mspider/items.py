# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Identity
from Mspider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT
class MspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def remove_splash(value):
    #去掉工作城市的斜线
    return value.replace("/", "")


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip()!="查看地图"]
    return "".join(addr_list)

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


class LagouItem(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
 )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_splash, handle_jobaddr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(",")
    )
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into lagou(title, url, url_object_id, salary, job_city, work_years, degree_need,
            job_type, publish_time, job_advantage, job_desc, job_addr, company_name, company_url,
            tags, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE salary=VALUES(salary), job_desc=VALUES(job_desc)
        """
        params = (
            self.get("title", ""),
            self.get("url", ""),
            self.get("url_object_id", ""),
            self.get("salary", ""),
            self.get("job_city", ""),
            self.get("work_years", ""),
            self.get("degree_need", ""),
            self.get("job_type", ""),
            self.get("publish_time", "0000-00-00"),
            self.get("job_advantage", ""),
            self.get("job_desc", ""),
            self.get("job_addr", ""),
            self.get("company_name", ""),
            self.get("company_url", ""),
            self.get("job_addr", ""),
            self.get("crawl_time", datetime.now().strftime(SQL_DATETIME_FORMAT))
        )

        return insert_sql, params

class LagouItemLoader(ItemLoader):
    default_input_processor = TakeFirst()
