# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os

class AmazoncspiderPipeline(object):
    def process_item(self, item, spider):
        d = item["directory"]
        if "/" in d:
            if not os.path.exists(os.path.dirname(d)):
                os.makedirs(os.path.dirname(d))
        with open(d+item["rankTime"]+".json","a",encoding="utf-8") as f:
            f.write(json.dumps(dict(item),ensure_ascii=False)+"\n")
        return item
