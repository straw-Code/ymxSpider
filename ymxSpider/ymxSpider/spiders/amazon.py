# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime as dt
from ymxSpider.items import YmxspiderItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    start_urls = ['https://www.amazon.cn/gp/new-releases/books/ref=zg_bsnr_unv_b_1_658394051_1']

    def changeT(t1):
        if int(t1) < 10:
            return "0" + t1
        return t1

    rankDate = dt.now()
    rankTime = str(rankDate.year) + changeT(str(rankDate.month)) + \
               changeT(str(rankDate.day))
    rankTime += changeT(str(rankDate.hour)) + changeT(str(rankDate.minute))
    print("排名时间:",rankTime)

    def parse(self, response):
        category = response.xpath('//span[@class="category"]//text()').extract()[0].strip()
        # 下一页链接：
        nextpage = response.xpath('//div[@class="a-text-center"]/ul/li[@class="a-normal"]/a/@href')
        if nextpage:
            nextpage = nextpage.extract()[0].strip()
            print("下一页：",nextpage)
            if nextpage[-1] == "2":
                yield scrapy.Request(nextpage)
        content = response.xpath('//li[@class="zg-item-immersion"]')
        for each in content:
            item = YmxspiderItem()
            # bookName = each.xpath('.//div[@class="p13n-sc-truncate"]')  # 不能用，源码修改了class属性
            bookName = each.xpath('.//div[contains(@class,"p13n-sc-truncate")]/text()').extract()[0].strip()
            # 作者
            author = each.xpath('.//span[@class="a-size-small a-color-base"]/text()').extract()[0].strip()
            # 图书排名：
            bookRank = each.xpath('.//span[@class="zg-badge-text"]/text()').extract()[0].strip()
            # 图书链接
            # link = each.xpath('.//span/a/@href').extract()[0].strip()
            link  = "https://www.amazon.cn" + each.xpath('.//span/a/@href').extract()[0].strip()
            # 评分：（有些没有）
            bookGrade = each.xpath('.//span[@class="a-icon-alt"]/text()').extract()
            # 评分人数：
            gradePeople = each.xpath('.//div/a[2]/text()').extract()
            if bookGrade:
                bookGrade = bookGrade[0].strip()
                gradePeople = gradePeople[0].strip()
            else:
                bookGrade = "未评分"
                gradePeople = "0"
            # 图书类型（平装、精装、电子书）
            bookType = each.xpath('.//span[@class="a-size-small a-color-secondary"]/text()').extract()[0].strip()
            # 价格：
            price = each.xpath('.//span[@class="p13n-sc-price"]/text()').extract()[0].strip()
            # 发行日期(销售排行榜没有该项)
            releaseDate = each.xpath('.//span[@class="zg-release-date"]/text()').extract()
            if releaseDate:
                # 发行日期
                item["releaseDate"] = releaseDate[0].strip()

            item["category"] = category
            item["bookName"] = bookName
            # 作者
            item["author"] = author
            # 图书排名：
            item["bookRank"] = bookRank
            # 图书链接
            item["link"] = link
            # 评分：（有些没有）
            item["bookGrade"] = bookGrade
            # 评分人数：
            item["gradePeople"] = gradePeople
            # 图书类型（平装、精装、电子书）
            item["bookType"] = bookType
            # 价格：
            item["price"] = price
            # 排名抓取时间
            item["rankTime"] = self.rankTime
            yield item



