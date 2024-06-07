import re
import json
import os
from datetime import datetime

import setting

# 番剧数据文件保存路径
bgmDataSavePath = setting.bgmDataSavePath

# alist网站的基础路径，用于后续截取alistPath
alistBasePath = setting.alistBasePath

# 番剧数据列表
bangumiList = []


def alistPathCut(path):
    """
    用于从"/home/onedrive/Sakiko/Bangumi/番剧名/readme.md"
    截取出"/Bangumi/番剧名"
    """
    match = re.search(r'{}(.*)/readme\.md'.format(alistBasePath), path)
    if match:
        return match.group(1)
    else:
        print('无法从 {} 中截取alistPath'.format(path))
        return ''


def bangumiIdCut(url):
    """
    从"https://bangumi.tv/subject/436745"
    截取出"436745"番剧id
    """
    match = re.search(r'/subject/(\d+)', url)
    if match:
        return match.group(1)
    else:
        print('无法从 {} 中截取番剧id'.format(url))
        return None


def push(data, pageInfo, urlInfo):
    """
    在main.py调用，将获取的番剧数据加入bangumiList
    data：获取的番剧数据
    pageInfo：使用其中的saveFile，以此来截取alistPath
    urlInfo: crawl_info中urlList的内容，判断source是否为bangumi，
        urlInfo中存在alistPath时，则不再从path中截取
    """
    # 来源不是bangumi则直接返回
    if urlInfo['source'] != 'bangumi':
        return

    # 准备 bangumi ID
    bangumiId = bangumiIdCut(urlInfo['url'])
    if not bangumiId:
        return

    # 准备 alistPath
    alistPath = ''
    if 'alistPath' in urlInfo:
        alistPath = urlInfo['alistPath']
    else:
        alistPath = alistPathCut(pageInfo['saveFile'])

    try:
        # 整理数据
        bangumiData = {
            "id": bangumiId,
            "alistPath": alistPath,
            "bgmUrl": data['MainPost']['BANGUMI_URL'],
            "img": data['MainPost']['BANGUMI_IMG'],
            "name": data['MainPost']['BANGUMI_NAME'],
            "chineseName": data['MainPost']['BANGUMI_CHINESE'],
            "episode": data['MainPost']['BANGUMI_EPISODE'],
            "date": data['MainPost']['BANGUMI_DATE'],
            "weekday": data['MainPost']['BANGUMI_WEEKDAY'],
            "score": data['MainPost']['BANGUMI_SCORE'],
            # "charsInfo": [{"img": img['BANGUMI_CHAR_IMG']} for img in data['MainPost']['PostImgs']],
            # "comments": [
            #     {
            #         "img": post['POST_USER_IMG'],
            #         "name": post['POST_USER_NAME'],
            #         "content": post['POST_CONTENT_P']
            #     } for post in data['RePosts']
            # ]
        }
        # 添加数据
        bangumiList.append(bangumiData)
    except Exception as e:
        print("{}{}在整理数据中缺少数据：{}"
              .format(pageInfo['saveFile'], urlInfo['url'], e))


def save(crawl_info_name):
    """
    在main.py调用，保存数据
    crawl_info_name：用于拼接保存的文件名
    """
    # 1.确保保存路径存在
    if not os.path.exists(bgmDataSavePath):
        os.makedirs(bgmDataSavePath)

    # 2.bangumiList 转为 json
    # 3.保存在 bgmDataSavePath+'bgm_data-'+crawl_info_name
    file_path = os.path.join(bgmDataSavePath, 'bgm_data-' + crawl_info_name)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(bangumiList, f, ensure_ascii=False)
            print('bangumiList保存成功：{}'.format(file_path))
    except Exception as e:
        print('保存数据时出错: {}, crawl_info_name: {}'.format(e, crawl_info_name))

    """ 4.修改 bgmDataSavePath 文件夹下的 config.json """
    # 读取文件
    config_path = os.path.join(bgmDataSavePath, 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except:
        config = {}

    # 检查bgmFileList是否存在且为列表
    if 'bgmFileList' not in config or not isinstance(config['bgmFileList'], list):
        config['bgmFileList'] = []

    # 更新 config.json
    # 准备数据
    fileName = 'bgm_data-' + crawl_info_name
    lastModified = datetime.now().isoformat()

    # 搜索fileName并修改lastModified，如果没有再append
    for bgmFile in config['bgmFileList']:
        if bgmFile['fileName'] == fileName:
            bgmFile['lastModified'] = lastModified
            break
    else:
        config["bgmFileList"].append({
            "fileName": fileName,
            "lastModified": lastModified,
            "showOnHome": False
        })

    # 保存文件
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False)
            print('config.json更新成功：{}'.format(config_path))
    except Exception as e:
        print('更新config.json时出错: {}, crawl_info_name: {}'.format(e, crawl_info_name))

    """ 修改 bgmDataSavePath 文件夹下的 config.json END """

    pass
