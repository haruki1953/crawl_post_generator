

bangumiList = []

def push(data, path, urlInfo):
    """
    在main.py调用，将获取的番剧数据加入bangumiList
    data：获取的番剧数据
    path：crawl_info中的saveFile，以此来截取alistPath
    urlInfo: crawl_info中urlList的内容，判断source是否为bangumi，
        urlInfo中存在alistPath时，则不再从path中截取
    """
    pass

def save(crawl_info_name):
    """
    在main.py调用，保存数据
    crawl_info_name：用于拼接保存的文件名
    """
    pass