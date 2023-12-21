# Crawl Post Generator

[English](./README.en.md) | [简体中文](./README.md)

It is primarily used for AList. The `crawl_info.json` file controls the web pages to be crawled, and the generated content is saved in the `readme.md` file in the AList mount folder. This allows the introduction content to be displayed when the AList folder is opened.

It supports custom crawling strategies and style templates, enabling the crawling and generation of multiple websites.

It supports the crawling and display of comments.

It supports responsive layout.

![image-20231221141737267](assets/image-20231221141737267.png)

![image-20231221142154914](assets/image-20231221142154914.png)

![image-20231221143709622](assets/image-20231221143709622.png)

![image-20231221143153354](assets/image-20231221143153354.png)

## How to Use

Ensure BeautifulSoup is installed: `pip install beautifulsoup4`

Configure `setting.py`, correctly map the crawling strategy and style template mapping dictionary, and set the path to save the crawling information json file.

If there are custom crawling strategies and style template modules, you can add them here. The ‘default’: default_template in the style template cannot be modified.

![image-20231221150837255](assets/image-20231221150837255.png)

Create a `crawl_info.json` file to control crawling and saving. The “source”: “source” in it should correspond to the key of the crawling strategy and style template mapping dictionary.

```
[
    {
        "saveFile": "/save path/readme.md",
        "urlList": [
            {
                "source": "source",
                "url": "web page link"
            }
        ]
    }
]
```

![image-20231221152328105](assets/image-20231221152328105.png) 

Run the python script `main.py` to start.

**Tips**

You can pass the path of the `crawl_info.json` file as a parameter when running `main.py`, and it will get the crawling information from this path.

You can put the `crawl_info.json` file in the AList mount folder for easy modification.

Through multiple `crawl_info.json` files and scheduled tasks, you can update the content at different periods. For example, write all the new episodes of October 23 in `crawl_info_23 October.json`, and you can easily control its update frequency after it is finished.

## Extension

Add custom modules to the `my_crawlers` package and `my_templates` package to add custom crawling strategies and style templates. After adding, you need to correctly map in `setting.py`.

**Crawling Strategy:** Add a custom module `xxx_crawler.py`, its main function should receive a web page link to crawl the web page, and return a dictionary containing thread data.

```python
threadData = {
    'SOURCE_URL': 'source website link',
    'SOURCE_IMG': 'source website icon',
    'SOURCE_NAME': 'source website name',
    'THREAD_URL': 'thread link',
    'TOGGLE_ID': 'used for the display and hiding of replies, cannot be repeated, can use thread id or random number',
    # Main post
    'myMainPost': { 
        'POST_USER_URL': 'main post link',
        'POST_USER_IMG': 'user avatar',
        'POST_user': 'username',
        'POST_CONTENT_P': 'post content',
        'myPostImgs': [
            {'POST_CONTENT_IMG':'post image'},
        ]
    }, 
    # Reply list
    'myRePosts': [
        {'POST_USER_URL': 'main post link',
         'POST_USER_IMG': 'user avatar',
         'POST_user': 'username',
         'POST_CONTENT_P': 'post content',
         'myPostImgs': [
            {'POST_CONTENT_IMG':'post image'},
        ]},
    ]
}
```

The keys in the dictionary with uppercase letters + underscores can be customized (can be added or deleted), and must correspond to the template.

**Style Template:** Add a custom module `xxx_template.py`, which should have the following five strings, please refer to other templates

```python
# Custom css
customCssOfHtml = ''''''
# Thread template
threadOfHtml = ''''''
# Main post template
mainpostOfHtml = ''''''
# Reply template, can be the same as the main post depending on the situation
repostOfHtml = ''''''
# Template for each image
imgOfHtml = ''''''
```