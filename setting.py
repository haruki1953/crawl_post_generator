# -*- coding: utf-8 -*-

# 导入爬取策略与样式模板
from my_templates import default_template, bangumi_template
from my_crawlers import cycg_crawler, bangumi_crawler

# 来源-爬取策略 映射字典
crawlersDict = {
    'cycg': cycg_crawler,
    'bangumi': bangumi_crawler,
}

# 来源-样式模板 映射字典
styleDict = {
    'default': default_template,
    'cycg' : default_template,
    'bangumi': bangumi_template,
}

# crawl_info.json 保存爬取信息的json文件的路径
crawl_info_json = './test/crawl_info.json'