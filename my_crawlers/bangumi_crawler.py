# -*- coding: utf-8 -*-

'''
针对bangumi网站爬取策略
获取一个番剧页面链接，返回一个字典
字典中以 大写字母+下划线 的键值可以自定义，但要与模板中对应
threadData = {
    'SOURCE_URL': '来源网站的链接',
    'SOURCE_IMG': '来源网站的图标',
    'SOURCE_NAME': '来源网站的名称',
    'THREAD_URL': '帖子的链接',
    'TOGGLE_ID': '用于回帖的显示与隐藏，不能重复 可以使用帖子id或随机数',
    # 番剧信息栏
    'myMainPost': { 
        'BANGUMI_URL': 'bangumi页面链接',
        'BANGUMI_IMG': '番剧图片',
        'BANGUMI_NAME': '番剧名',
        'BANGUMI_CONTENT': '番剧介绍内容',
        'myPostImgs': [
            {'BANGUMI_CHAR_IMG':'角色的图片'},
        ]
    }, 
    # 吐槽箱里的多个评论，因为吐槽箱没有图片，所以myPostImgs为空就行
    'myRePosts': [
        {'POST_USER_URL': '链接',
         'POST_USER_IMG': '用户头像',
         'POST_USER_NAME': '用户名',
         'POST_CONTENT_P': '帖子内容',
         'myPostImgs': []
         },
    ]
}
'''

import urllib.request
import hashlib
import re
from bs4 import BeautifulSoup



def open_url(url):#打开链接
    html = urllib.request.urlopen(url).read().decode()
    return html



def split_thread_content(threadHtml):
    """
    初步整理页面html
    切割划分番剧信息与吐槽箱评论列表，返回装着Soup的字典
    threadContentSoup = {
        # 番剧信息
        'mainPostSoup': "番剧信息的Soup", 
        # 评论列表
        'rePostsSoup': [
            "评论1的Soup",
            "评论2的Soup",
        ]
    }
    """
    # 创建一个空字典
    threadContentSoup = {}
    # 使用BeautifulSoup库解析HTML内容
    soup = BeautifulSoup(threadHtml, 'html.parser')
    
    # 找到主要信息
    wrapperNeue = soup.find('div', {'id': 'wrapperNeue'})

    # 找到吐槽箱
    commentBox = wrapperNeue.find('div', {'id': 'comment_box'})
    # 找到所有评论，class="item clearit"并有data-item-user属性的元素
    allComments = []
    for comment in commentBox.find_all('div', {'class': 'item clearit'}):
        # 如果该标签class属性为"item clearit"并且有data-item-user属性，则将其添加到allComments列表中
        if comment.has_attr('data-item-user'):
            allComments.append(comment)

    threadContentSoup['mainPostSoup'] = wrapperNeue
    threadContentSoup['rePostsSoup'] = allComments

    return threadContentSoup



def get_mainpost_data(postSoup: BeautifulSoup, threadData):
    """
    根据postSoup获取番剧数据，需要threadData以获取必要数据（拼接链接）
    参数postSoup为番剧信息html的Soup对象
    返回番剧数据 'myMainPost': { 
    'BANGUMI_URL': 'bangumi页面链接',
    'BANGUMI_IMG': '番剧图片',
    'BANGUMI_NAME': '番剧名',
    'BANGUMI_CONTENT': '番剧介绍内容',
    'myPostImgs': [
        {'BANGUMI_CHAR_IMG':'角色的图片'},
    ]}
    """
    # 初始化主帖数据
    myMainPost = {}
    
    # headerSubject里的h1标签里的a标签保存着番剧名与链接
    bangumiName = postSoup.find('div', {'id': 'headerSubject'}).find('h1').find('a')
    """ BANGUMI_URL """
    myMainPost['BANGUMI_URL'] = threadData['SOURCE_URL'] + bangumiName['href']
    """ BANGUMI_NAME """
    myMainPost['BANGUMI_NAME'] = bangumiName.decode_contents()

    """ BANGUMI_IMG """
    # bangumiInfo里的img就是番剧图片
    bangumiImg = postSoup.find('div', {'id': 'bangumiInfo'}).find('img')
    myMainPost['BANGUMI_IMG'] = bangumiImg['src']

    """ BANGUMI_CONTENT """
    # id="subject_summary"的div标签里保存着番剧介绍内容
    bangumiContent = postSoup.find('div', {'id': 'subject_summary'})
    myMainPost['BANGUMI_CONTENT'] = bangumiContent.decode_contents()

    """ myPostImgs """
    myMainPost['myPostImgs'] = []
    # id="browserItemList"的ul标签里保存着角色图片列表
    bangumiCharImgList = postSoup.find('ul', {'id': 'browserItemList'})
    # 使用正则表达式匹配图片链接
    # background-image:url('//lain.bgm.tv/pic/crt/g/73/4a/134703_crt_nOncx.jpg?r=1699789465')
    imgUrlList = re.findall(r'background-image:url\(\'(.*?)\'\)', str(bangumiCharImgList))
    for imgUrl in imgUrlList:
        myMainPost['myPostImgs'].append({'BANGUMI_CHAR_IMG': imgUrl})


    return myMainPost



def get_repost_data(postSoup: BeautifulSoup, threadData):
    """
    根据postSoup获取评论数据
    返回评论数据 'myRePost': {
    'POST_USER_URL': '链接',
    'POST_USER_IMG': '用户头像',
    'POST_USER_NAME': '用户名',
    'POST_CONTENT_P': '帖子内容',
    'myPostImgs': []
    },
    因为吐槽箱里的评论没有图片，所以myPostImgs为空
    """
    myRePost = {'myPostImgs': []}

    # class="avatar"的a标签里有用户链接与图片
    avatar = postSoup.find('a', {'class': 'avatar'})
    """ POST_USER_URL """
    myRePost['POST_USER_URL'] = threadData['SOURCE_URL'] + avatar['href']
    """ POST_USER_IMG """
    # 使用正则表达式匹配图片链接
    myRePost['POST_USER_IMG'] = re.search(r'background-image:url\(\'(.*?)\'\)', str(avatar)).group(1)

    # class="text"的div标签中保存着用户名与评论内容
    text = postSoup.find('div', {'class': 'text'})
    """ POST_USER_NAME """
    # a标签里保存着用户名
    myRePost['POST_USER_NAME'] = text.find('a').decode_contents()
    """ POST_CONTENT_P """
    # p标签里保存着评论内容
    myRePost['POST_CONTENT_P'] = text.find('p').decode_contents()
    

    return myRePost



def main(threadUrl):
    # 初始化帖子数据
    threadData = {
        'SOURCE_URL': 'https://bangumi.tv',
        'SOURCE_IMG': 'https://bangumi.tv/img/rc3/logo_2x.png',
        'SOURCE_NAME': 'bangumi',
        'THREAD_URL': threadUrl,
        'TOGGLE_ID': hashlib.sha256(threadUrl.encode()).hexdigest(), # 使用链接的哈希值充当
    }

    # 获取bangumi页面的html
    threadHtml = open_url(threadUrl)

    # 整理番剧信息与评论列表
    threadContentSoup = split_thread_content(threadHtml)

    # 获取番剧数据
    threadData['myMainPost'] = get_mainpost_data(threadContentSoup['mainPostSoup'], threadData)

    # 获取评论
    threadData['myRePosts'] = []
    for postSoup in threadContentSoup['rePostsSoup']:
        threadData['myRePosts'].append(get_repost_data(postSoup, threadData))

    return threadData


# #测试
# # 获取bangumi页面的html
# threadData = main('https://bangumi.tv/subject/424379')

# # 打开一个文件，如果不存在则创建  
# with open('./bgmtest_data.html', 'w', encoding='utf-8') as file:  
#     # 写入字符串到文件  
#     file.write(str(threadData))
