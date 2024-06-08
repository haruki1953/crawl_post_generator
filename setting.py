# -*- coding: utf-8 -*-

# 导入爬取策略
from crawlers import bangumi, cycg

# 来源-爬取策略 映射字典
crawlersDict = {
    'cycg': cycg,
    'bangumi': bangumi
}

# crawl_info.json 保存爬取信息的json文件的路径
crawl_info_json = './test/crawl_info.json'

# 番剧数据文件保存路径
bgmDataSavePath = './data'

# alist网站的基础路径，用于截取alistPath
alistBasePath = '/home/onedrive/Sakiko'
# alist网站网址，用于与截取的路径拼接
alistWebUrl = 'https://bangumi.sakiko.top'
