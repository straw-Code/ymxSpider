# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
class YmxspiderPipeline(object):
    def process_item(self, item, spider):
        # if os.path.exists(item["category"]+".json"):
            # os.remove(item["category"]+".json")
        with open(item["category"]+item["rankTime"]+".json","a",encoding="utf-8") as f:
            f.write(json.dumps(dict(item),ensure_ascii=False)+"\n")
        return item
