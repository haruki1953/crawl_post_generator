# -*- coding: utf-8 -*-

'''
针对cycg网站爬取策略
获取一个帖子的网页链接，返回一个帖子的数据
字典中以 大写字母+下划线 的键值可以自定义，但要与模板中对应
threadData = {
    'SOURCE_URL': '来源网站的链接',
    'SOURCE_IMG': '来源网站的图标',
    'SOURCE_NAME': '来源网站的名称',
    'THREAD_URL': '帖子的链接',
    'TOGGLE_ID': '用于回帖的显示与隐藏，不能重复 可以使用帖子id或随机数',
    # 主帖
    'MainPost': { 
        'POST_USER_URL': '主贴链接',
        'POST_USER_IMG': '用户头像',
        'POST_USER_NAME': '用户名',
        'POST_CONTENT_P': '帖子内容',
        'PostImgs': [
            {'POST_CONTENT_IMG':'帖子的图片'},
        ]
    }, 
    # 回帖列表
    'RePosts': [
        {'POST_USER_URL': '主贴链接',
         'POST_USER_IMG': '用户头像',
         'POST_USER_NAME': '用户名',
         'POST_CONTENT_P': '帖子内容',
         'PostImgs': [
            {'POST_CONTENT_IMG':'帖子的图片'},
        ]},
    ]
}
'''

import urllib.request
import hashlib
import re
from bs4 import BeautifulSoup


def open_url(url):  # 打开链接
    html = urllib.request.urlopen(url).read().decode()
    return html


def split_thread_content(threadHtml):
    """
    初步整理页面html
    切割划分帖子的主帖与回帖列表，返回装着Soup的字典
    threadContentSoup = {
        # 主帖
        'mainPostSoup': "主帖的Soup", 
        # 回帖列表
        'rePostsSoup': [
            "回帖1的Soup",
            "回帖2的Soup",
        ]
    }
    """
    # 创建一个空字典
    threadContentSoup = {}
    # 使用BeautifulSoup库解析HTML内容
    soup = BeautifulSoup(threadHtml, 'html.parser')
    # 获取帖子的主体内容
    postlist = soup.find('div', {'id': 'postlist'})
    # 获取所有的回帖和主帖
    all_posts = []
    for post in postlist.find_all('div'):
        # 如果该标签有id属性并且以'post_'开头且后面跟着数字，则将其添加到all_posts列表中
        if post.has_attr('id') and re.match(r'post_\d+', post['id']):
            all_posts.append(post)
    # 将主帖和回帖列表存储在threadContentSoup字典中，第一个是主帖，其余的是回帖
    threadContentSoup['mainPostSoup'] = all_posts[0]
    threadContentSoup['rePostsSoup'] = all_posts[1:]

    return threadContentSoup


def get_mainpost_data(postSoup, threadData):
    """
    根据postSoup获取主帖数据，需要threadData以获取必要数据
    参数postSoup为主帖html的Soup对象
    返回主帖数据 MainPost = { 
    'POST_USER_URL': '主贴链接',
    'POST_USER_IMG': '用户头像',
    'POST_USER_NAME': '用户名',
    'POST_CONTENT_P': '帖子内容',
    'PostImgs': [
        {'POST_CONTENT_IMG':'帖子的图片链接'},
    ]}
    """
    # 初始化主帖数据
    MainPost = {}

    """用户信息获取准备"""
    # 找到favatar_div标签，这是帖子内容的标签
    favatar_div = False
    for div in postSoup.find_all('div'):
        # 如果该标签有id属性并且以'postmessage_'开头且后面跟着数字，则将其保存
        if div.has_attr('id') and re.match(r'favatar\d+', div['id']):
            # 保存div标签
            favatar_div = div
            break
    # 如果找不到favatar_div，抛出错误
    if not favatar_div:
        raise Exception('页面{}中的{}用户信息缺失，未找到id="favatar数字"的div标签'.format(
            threadData['THREAD_URL'], postSoup['id']))

    """帖子内容获取准备"""
    # 找到postmessage_td标签，这是帖子内容的标签
    postmessage_td = False
    for td in postSoup.find_all('td'):
        # 如果该标签有id属性并且以'postmessage_'开头且后面跟着数字，则将其保存
        if td.has_attr('id') and re.match(r'postmessage_\d+', td['id']):
            # 保存td标签
            postmessage_td = td
            break
    # 如果找不到postmessage_td，抛出错误
    if not postmessage_td:
        raise Exception('页面{}中的{}帖子内容缺失，未找到id="postmessage_数字"的td标签'.format(
            threadData['THREAD_URL'], postSoup['id']
        ))

    """POST_USER_URL"""
    # 通过帖子链接+帖子id来定位到帖子
    MainPost['POST_USER_URL'] = threadData['THREAD_URL'] + '#' + postSoup['id']

    """POST_USER_IMG"""
    # 在favatar_div用户信息中，找到class为avatar的div，里面就有用户头像图片
    avatar_div = favatar_div.find('div', class_='avatar')
    tag_img = avatar_div.find('img')
    MainPost['POST_USER_IMG'] = tag_img['src']

    """POST_USER_NAME"""
    # 在favatar_div用户信息中，找到class为authi的div，里面的a标签的内容就是用户名
    authi_div = favatar_div.find('div', class_='authi')
    tag_a = authi_div.find('a')
    MainPost['POST_USER_NAME'] = tag_a.decode_contents()

    """PostImgs"""
    # ignore_js_op下的图片，并提取POST_CONTENT_IMG，链接需要和域名拼接，添加到MainPost
    MainPost['PostImgs'] = []
    for ignore_js_op in postmessage_td.find_all('ignore_js_op'):
        img = ignore_js_op.find('img')
        imgUrl = threadData['SOURCE_URL'] + '/' + img['file']
        MainPost['PostImgs'].append({
            'POST_CONTENT_IMG': imgUrl
        })

    """POST_CONTENT_P"""
    # 在postmessage_td中找到<div class="quote">中的<blockquote>，这是回复信息，最后要和内容合并
    replyStr = ''
    quote_div = postmessage_td.find('div', class_='quote')
    if quote_div:
        blockquote = quote_div.find('blockquote')
        if blockquote:  # 删除所有子标签，保留文字和br标签（内容可能在br标签内）
            for tag in blockquote.find_all(True):
                if tag.name not in ['br',]:
                    tag.extract()
            # 提取内容并处理
            replyStr = blockquote.decode_contents()
            # 使用正则表达式删除开头和结尾的br标签
            replyStr = re.sub(r'^(\s*(<br>|<br/>|</br>)\s*)+', '', replyStr)
            replyStr = re.sub(r'(\s*(<br>|<br/>|</br>)\s*)+$', '', replyStr)
            # 使用正则表达式删除连续的br标签，最多保留一个
            replyStr = re.sub(r'(\s*(<br>|<br/>|</br>)\s*)+',
                              '<br/>', replyStr)
            # 最后添加引用标签
            replyStr = '<blockquote>' + replyStr + '</blockquote>'
    # 获取并整理内容
    # 删除不在保留列表中的所有子标签，保留下直接包裹的文字
    for tag in postmessage_td.find_all(True):
        if tag.name not in ['a', 'img', 'br']:
            tag.extract()
    # 删除img标签中的所有属性，只保留src，并拼接完善
    for img in postmessage_td.find_all('img'):
        img.attrs = {'src': threadData['SOURCE_URL'] + '/' + img['src']}
    # 删除a标签中的所有属性，只保留href
    for a in postmessage_td.find_all('a'):
        a.attrs = {'href': a['href']}
    # 获取td标签的内容的字符串形式，不包含td标签
    content = postmessage_td.decode_contents()
    # 使用正则表达式删除开头和结尾的br标签
    content = re.sub(r'^(\s*(<br>|<br/>|</br>)\s*)+', '', content)
    content = re.sub(r'(\s*(<br>|<br/>|</br>)\s*)+$', '', content)
    # 使用正则表达式删除连续的br标签，最多保留一个
    content = re.sub(r'(\s*(<br>|<br/>|</br>)\s*)+', '<br/>', content)
    # 给内容的最开始加上回复信息
    content = replyStr + content
    # 保存到MainPost
    MainPost['POST_CONTENT_P'] = content

    # # 打印获取到内容
    # import pprint
    # # print(MainPost)
    # pprint.pprint(MainPost)

    return MainPost


def get_repost_data(postSoup, threadData):
    """
    根据html获取回帖数据
    在cycg中和主帖的策略是一样的
    """
    return get_mainpost_data(postSoup, threadData)


def main(threadUrl):
    # 初始化帖子数据
    threadData = {
        'SOURCE_URL': 'https://www.cycg.xyz',
        'SOURCE_IMG': 'https://www.cycg.xyz/template/acgi_c1/images/logo.png',
        'SOURCE_NAME': 'Sperteの次元茶馆',
        'THREAD_URL': threadUrl,
        # 使用链接的哈希值充当
        'TOGGLE_ID': hashlib.sha256(threadUrl.encode()).hexdigest(),
    }

    # 获取帖子的html
    threadHtml = open_url(threadUrl)

    # 帖子的主帖与回帖列表
    threadContentSoup = split_thread_content(threadHtml)

    # 获取主帖数据
    threadData['MainPost'] = get_mainpost_data(
        threadContentSoup['mainPostSoup'], threadData)

    # 获取回帖
    threadData['RePosts'] = []
    for postSoup in threadContentSoup['rePostsSoup']:
        threadData['RePosts'].append(get_repost_data(postSoup, threadData))

    return threadData
