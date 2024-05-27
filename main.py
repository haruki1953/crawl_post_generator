# -*- coding: utf-8 -*-

import re
import os
import json

# 导入设置数据
import setting


""" 模板拼接 """
# 自定义替换函数，用于将模板字符串中的占位符替换为数据字典中对应的值
def custom_replace(templateStr, data):
    for key, value in data.items():
        templateStr = templateStr.replace('{' + key + '}', str(value))
    return templateStr

# 格式化图片列表
def format_images(img_list, template):
    images = ''
    for img in img_list:
        # 使用自定义替换函数格式化每个图片，并添加到结果字符串中
        images += custom_replace(template.imgOfHtml, img)
    return images

# 格式化主帖
def format_mainpost(post, template):
    # 生成图片内容
    post['myPostImgs'] = format_images(post['myPostImgs'], template)
    # 使用自定义替换函数格式化帖子数据，并将格式化的图片列表插入到结果字符串中
    post_html = custom_replace(template.mainpostOfHtml, post)
    return post_html

# 格式化回帖 
def format_repost(post, template):
    # 生成图片内容
    post['myPostImgs'] = format_images(post['myPostImgs'], template)
    # 使用自定义替换函数格式化帖子数据，并将格式化的图片列表插入到结果字符串中
    post_html = custom_replace(template.repostOfHtml, post)
    return post_html

# 格式化回帖列表
def format_reposts(post_list, template):
    posts = ''
    for post in post_list:
        # 使用format_post函数格式化每个帖子，并添加到结果字符串中
        posts += format_repost(post, template)
    return posts

# 格式化主题帖
def format_thread(threadData, template):
    # 生成主帖和回帖的内容
    threadData['myMainPost'] = format_mainpost(threadData['myMainPost'], template)
    threadData['myRePosts'] = format_reposts(threadData['myRePosts'], template)
    # 再使用自定义替换函数格式化主题帖数据
    thread_html = custom_replace(template.threadOfHtml, threadData)
    return thread_html

# 生成HTML
def generate_html(threadDataList):
    # 保存帖子
    threads = ''
    # 保存自定义css
    customCss = ''
    # 记录已保存的自定义css，避免重复保存
    savedCss = []

    for threadData in threadDataList:
        # 使用format_thread函数格式化每个主题帖，并添加到结果字符串中
        threads += format_thread(threadData['data'], setting.styleDict[threadData['source']])
        # 如果对应css未保存，则保存
        if threadData['source'] not in savedCss:
            savedCss.append(threadData['source'])
            customCss += setting.styleDict[threadData['source']].customCssOfHtml
    # 生成最终的HTML
    html = custom_replace(setting.styleDict['default'].allOfHtml, 
                          {'myThreads': threads, 'myCustomCss':customCss})
    # 最后删除空行
    html = re.sub(r'\n\s*\n', '\n', html)
    return html
""" 模板拼接 END """



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



def main(crawlInfoList):
    # 遍历爬取信息 pageInfo页面信息字典
    for pageInfo in crawlInfoList:
        # 创建空帖子数据列表，其中将保存帖子信息字典，data为帖子数据，source为帖子来源
        # threadDataList = [{'data': '帖子数据', 'source': '帖子来源'}, ...]
        threadDataList = [] 
        
        try:
            # 遍历页面信息字典的urlList urlInfo
            for urlInfo in pageInfo['urlList']:
                # 根据urlInfo中的soure调用爬取策略，传入url，得到其返回的帖子数据
                try:
                    threadData = setting.crawlersDict[urlInfo['source']].main(urlInfo['url'])
                except Exception as e:
                    print("urlInfo:", urlInfo)
                    print("发生了一个错误: {}".format(e))
                    # 发生错threadData设为False，帖子数据将不会被保存
                    threadData = False
                if threadData:
                    # 如果爬取成功，保存data为帖子数据，source为帖子来源
                    threadDataList.append({'data': threadData, 'source': urlInfo['source']})
                    
                    """ bangumi_list """
                    # 调用 bangumi_list 添加数据
                    """ bangumi_list END """

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

    # 也可以通过命令行传递crawl_info.json文件路径
    if len(sys.argv) > 1:
        crawl_info_json = sys.argv[1]
    
    try:
        # 打开JSON文件，获取crawlInfoList
        with open(crawl_info_json, 'r', encoding='utf-8') as f:
            # 使用json.load()方法将文件中的JSON数据解析为列表
            crawlInfoList = json.load(f)
        # main函数开始执行
        main(crawlInfoList)

        """ bangumi_list """
        # 根据bash执行时的参数判断是否保存bangumi_list
        # 调用 bangumi_list 保存数据
        """ bangumi_list END """

    except FileNotFoundError:
        print("错误：文件 {} 未找到。".format(crawl_info_json))
    except json.JSONDecodeError:
        print("错误：无法解析文件 {} 中的JSON。".format(crawl_info_json))
    except Exception as e:
        print("crawl_info_json: ", crawl_info_json)
        print("发生了一个错误: {}".format(e))

    