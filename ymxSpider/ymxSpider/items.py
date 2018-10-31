# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YmxspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 类别
    category = scrapy.Field()
    # 书名：
    bookName = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 图书排名：
    bookRank = scrapy.Field()
    # 图书链接
    link = scrapy.Field()
    # 评分：（有些没有）
    bookGrade = scrapy.Field()
    # 评分人数：
    gradePeople = scrapy.Field()
    # 图书类型（平装、精装、电子书）
    bookType = scrapy.Field()
    # 价格：
    price = scrapy.Field()
    # 发行日期
    releaseDate = scrapy.Field()
    # 排名抓取时间
    rankTime = scrapy.Field()
