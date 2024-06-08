# -*- coding: utf-8 -*-

import re
import os
import json

# 导入设置数据
import setting
import bangumi_list

# 模板引擎
from jinja2 import Environment, FileSystemLoader


def generate_html(threadDataList):
    # 生成HTML
    # threadDataList = [{'data': '帖子数据', 'source': '帖子来源'}, ...]

    # 设置模板文件夹
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    # 加载主模板
    template = env.get_template('main.html')

    # 渲染模板并传入数据
    html = template.render(threadDataList=threadDataList)

    # 最后删除空行
    # **注意注意：** 最后删除空行是必须的，否则alist的readme可能不会将其解析为html
    html = re.sub(r'\n\s*\n', '\n', html)
    return html


def save_html(path, string):
    """
    要检查路径是否存在，不存在则输出信息并返回
    并根据文件是否存在正确保存，保存在文件的<my-html>标签中
    """

    directory = os.path.dirname(path)
    # 检查文件夹是否存在
    if not os.path.exists(directory):
        print("发生了一个错误: 文件夹 {} 不存在".format(directory))
        return

    # 检查文件是否存在
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as file:
            file.write('<my-html></my-html>\n')
        print("文件 {} 已创建".format(path))

    # 读取文件内容
    with open(path, 'r', encoding='utf-8') as file:
        contents = file.read()

    # 查找并修改<my-html>标签的内容
    pattern = re.compile(r'<my-html>.*?</my-html>', re.DOTALL)
    replacement = '<my-html>{}</my-html>'.format(string)
    new_contents, num_subs_made = pattern.subn(replacement, contents)

    if num_subs_made == 0:
        new_contents += '\n' + replacement

    # 将修改后的内容写回文件
    with open(path, 'w', encoding='utf-8') as file:
        file.write(new_contents)
    print("文件 {} 已更新".format(path))


def main(crawlInfoList, stopHtml=False):
    # 遍历爬取信息 pageInfo页面信息字典
    for pageInfo in crawlInfoList:
        """
        pageInfo: {
            'saveFile': 'html保存至的文件', 
            'urlList': [{
                "source": "来源 bangumi、cycg",
                "url": "链接https://bangumi.tv/subject/467803"
            }, ...]
        }
        """
        # 创建空帖子数据列表，其中将保存帖子信息字典，data为帖子数据，source为帖子来源
        # threadDataList = [{'data': '帖子数据', 'source': '帖子来源'}, ...]
        threadDataList = []

        try:
            # 遍历页面信息字典的urlList
            for urlInfo in pageInfo['urlList']:
                # 根据urlInfo中的soure调用爬取策略，传入url，得到其返回的帖子数据
                try:
                    threadData = setting.crawlersDict[urlInfo['source']].main(
                        urlInfo['url'])
                except Exception as e:
                    print("urlInfo:", urlInfo)
                    print("发生了一个错误: {}".format(e))
                    # 发生错threadData设为False，帖子数据将不会被保存
                    threadData = False
                if threadData:
                    # 如果爬取成功，保存data为帖子数据，source为帖子来源
                    threadDataList.append(
                        {'data': threadData, 'source': urlInfo['source']})

                    """ bangumi_list """
                    # 调用 bangumi_list 添加数据
                    bangumi_list.push(threadData, pageInfo, urlInfo)
                    """ bangumi_list END """

            if stopHtml:  # 禁用html保存时跳过保存
                continue

            # 调用html模板拼接函数，返回整个页面html字符串
            htmlStr = generate_html(threadDataList)

            # 调用保存函数
            save_html(pageInfo['saveFile'], htmlStr)

        except Exception as e:
            print("pageInfo: ", pageInfo)
            print("发生了一个错误: {}".format(e))


if __name__ == '__main__':
    import sys

    # crawl_info_json为保存爬取信息的json文件的路径，默认为setting里设置的
    crawl_info_json = setting.crawl_info_json

    # 是否启用bangumi-list保存数据
    enableBangumiList = False
    # 是否禁用html保存
    stopHtml = False

    if len(sys.argv) > 1:
        # 也可以通过命令行传递crawl_info.json文件路径
        crawl_info_json = sys.argv[1]

    if len(sys.argv) > 2:
        if sys.argv[2] == 'BL':
            # 第二参数为'BL'时启用bangumi-list
            enableBangumiList = True
        elif sys.argv[2] == 'onlyBL':
            # 第二参数为'onlyBL'时不保存html
            enableBangumiList = True
            stopHtml = True

    try:
        # 打开JSON文件，获取crawlInfoList
        with open(crawl_info_json, 'r', encoding='utf-8') as f:
            # 使用json.load()方法将文件中的JSON数据解析为列表
            crawlInfoList = json.load(f)
        # main函数开始执行
        main(crawlInfoList, stopHtml)

        """ bangumi_list """
        # 根据bash执行时的参数判断是否保存bangumi_list
        if enableBangumiList:
            # 调用 bangumi_list 保存数据，参数为文件名
            bangumi_list.save(os.path.basename(crawl_info_json))
        """ bangumi_list END """

    except FileNotFoundError:
        print("错误：文件 {} 未找到。".format(crawl_info_json))
    except json.JSONDecodeError:
        print("错误：无法解析文件 {} 中的JSON。".format(crawl_info_json))
    except Exception as e:
        print("crawl_info_json: ", crawl_info_json)
        print("发生了一个错误: {}".format(e))
