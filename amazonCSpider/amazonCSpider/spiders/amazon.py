# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime as dt
from amazonCSpider.items import AmazoncspiderItem
import re

class AmazonSpider(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']

    # start_urls = ['https://www.amazon.cn/gp/new-releases/books/658399051']  # 子目录测试
    start_urls = ['https://www.amazon.cn/gp/new-releases/books/ref=zg_bsnr_unv_b_1_658394051_1']  # 图书目录

    rules = (
        Rule(LinkExtractor(allow=r'^https://www.amazon.cn/gp/new-releases/books/\d+?$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'^https://www\.amazon\.cn/gp/new-releases/books/?[\s\S]*?\?ie=UTF8&pg=2$'), callback='parse_item', follow=True),
    )


    def changeT(t1):
        if int(t1) < 10:
            return "0" + t1
        return t1

    rankDate = dt.now()
    rankTime = str(rankDate.year) + changeT(str(rankDate.month)) + \
               changeT(str(rankDate.day))
    rankTime += changeT(str(rankDate.hour)) + changeT(str(rankDate.minute))
    print("排名时间:",rankTime)

    def filter_item(self,info):
        if info:
            return info[0].strip()
        return "无"


    def parse_item(self, response):
        # category = response.xpath('//span[@class="category"]//text()').extract()[0].strip()  #　有些页面没有该属性
        # 以下写法可能分为两部分
        category = response.xpath('//h1[@class="a-size-large a-spacing-medium zg-margin-left-15 a-text-bold"]//text()').extract()
        if category:
            category = "".join(category)
        else:
            category = "无"
        print("调用ing=============",response.url)

        # 该页面目录的获取
        num = 0
        while num < 6:
            xpath_d = '//ul[@id="zg_browseRoot"]'+ "/ul" * num + "//li/span/text()"
            directory = response.xpath(xpath_d).extract()
            if not directory:
                # print("========层数：",num)
                break
            directory1 = directory
            num += 1

        directory2 = ""
        for i in range(num-1):
            xpath_d = '//ul[@id="zg_browseRoot"]' + "/ul" * i + "/li/a/text()"
            directory2 += response.xpath(xpath_d).extract()[0].strip() + "/"
        directory = directory2 + directory1[0].strip()
        # print(directory)

        content = response.xpath('//li[@class="zg-item-immersion"]')
        for each in content:
            item = AmazoncspiderItem()
            # bookName = each.xpath('.//div[@class="p13n-sc-truncate"]')  # 不能用，源码修改了class属性
            bookName = each.xpath('.//div[contains(@class,"p13n-sc-truncate")]/text()').extract()

            # 作者
            author = each.xpath('.//span[@class="a-size-small a-color-base"]/text()').extract()
            # 图书排名：
            bookRank = each.xpath('.//span[@class="zg-badge-text"]/text()').extract()
            # 图书链接
            # link = each.xpath('.//span/a/@href').extract()[0].strip()
            link = each.xpath('.//span/a/@href').extract()
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
            bookType = each.xpath('.//span[@class="a-size-small a-color-secondary"]/text()').extract()
            # 价格：
            price = each.xpath('.//span[@class="p13n-sc-price"]/text()').extract()
            # 发行日期(销售排行榜没有该项)
            releaseDate = each.xpath('.//span[@class="zg-release-date"]/text()').extract()

            item["category"] = category
            item["bookName"] = self.filter_item(bookName)
            # 作者
            item["author"] = self.filter_item(author)
            # 图书排名：
            item["bookRank"] = self.filter_item(bookRank)
            # 图书链接
            item["link"] = "https://www.amazon.cn" + self.filter_item(link)
            # 评分：（有些没有）
            item["bookGrade"] = bookGrade
            # 评分人数：
            item["gradePeople"] = gradePeople
            # 图书类型（平装、精装、电子书）
            item["bookType"] = self.filter_item(bookType)
            # 价格：
            item["price"] = self.filter_item(price)
            # 发行日期(销售排行榜没有该项)
            item["releaseDate"] = self.filter_item(releaseDate)
            # 排名抓取时间
            item["rankTime"] = self.rankTime
            # 目录
            item["directory"] = directory
            # 排名页面url
            item["rankurl"] = response.url
            yield item




    # def parse_exist(self, response):
    #     reg = re.compile(r"https://www\.amazon\.cn/gp/new-releases/books/?[\s\S]*?\?ie=UTF8&pg=\d+")
    #     link_page = reg.findall(response.text)
    #     if not link_page:
    #         print("=======================无下一页:",response.url,"====**",link_page,"++=====")
    #         self.parse_item(response)



    def parse_start_url(self, response):
        print("起始页》》》》》》》》》》》",response.url)
        # yield self.parse_item(response)  # 失败，self.parse_item是生成器
        for i in self.parse_item(response):
            yield i








