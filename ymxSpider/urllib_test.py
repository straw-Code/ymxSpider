import re
import urllib
from lxml import etree
from bs4 import BeautifulSoup as bs

# res = urllib.request.urlopen("https://www.amazon.cn/gp/new-releases/books/ref=zg_bsnr_unv_b_1_658394051_1")
# # print(res.read().decode())
# html = res.read().decode()

# xpath 的使用
# parse_html = etree.HTML(html)
# book = parse_html.xpath('//li[@class="zg-item-immersion"]')
# for each in book:
#     bookName = each.xpath('.//div[contains(@class,"p13n-sc-truncate")]/text()')
#     print(bookName)

# BeautifulSoup 的使用
# soup = bs(html,"lxml")
# book = soup.find_all("li",{"class","zg-item-immersion"})
# print(book)

a =  "<li>&#x6545;&#x5BAB;&#x65E5;&#x5386;(&#x516C;&#x5386;2019&#x5E74;)(&#x7CBE;)</li>"
soup1 = bs(a,"lxml")
book1 = soup1.find_all("li")
book2 = soup1.find_all(text=re.compile("故宫"))
print(book1,book2)  # [<li>故宫日历(公历2019年)(精)</li>] ['故宫日历(公历2019年)(精)']


