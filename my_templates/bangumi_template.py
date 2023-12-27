# -*- coding: utf-8 -*-

# 自定义css
customCssOfHtml = '''
<!-- bangumi自定义css --> 
<style type="text/css">
    .bangumi_container {
        display: flex;
        flex-wrap: wrap;
    }

    .bangumi_imgbox {
        flex: 1;
        padding: 0 10px;
    }

    .bangumi_content {
        flex: 3;
        padding: 0 10px;
    }

    .bangumi_img {
        display: block !important;
        margin: 0 auto;
        width: 200px;
        border-radius: 10px;
    }

    .bangumi_info {
        margin: 0 auto !important;
        margin-top: 10px !important;
        width: 200px;
        list-style-type: none;
        padding-inline-start: 0px !important;
        line-height: 24px !important;
    }

    .bangumi_tip {
        color: #666;
    }

    .bangumi_char_img {
        width: 48px;
        /* height: 48px; */
        object-fit: cover;
        border-radius: 10px;
        margin: 3px
    }

    @media (max-width: 600px) {
        .bangumi_info {
            flex-basis: 100%;
        }

        .bangumi_imgbox {
            flex-basis: 100%;
        }
    }
</style>
'''

# 主题帖的模板
threadOfHtml = '''
<div class="my_thread">
    <div class="my_source">
        <!-- 来源 -->
        <a href="{THREAD_URL}" target="_blank" class="my_nameBox my_a">
            <img src="{SOURCE_IMG}" height="44px" title="{SOURCE_NAME}">
            <!-- <span class="my_name">{SOURCE_NAME}</span> -->
        </a>
    </div>
    {myMainPost}
    <button id="{TOGGLE_ID}_toggleButton" class="my_button">吐槽 显示/隐藏</button>
    <div id="{TOGGLE_ID}_targetElement" class="my_comments" style="display: none;">
        {myRePosts}
    </div>
    <script>
        document.getElementById('{TOGGLE_ID}_toggleButton').addEventListener('click', function () {
            document.getElementById('{TOGGLE_ID}_targetElement').style.display = document.getElementById('{TOGGLE_ID}_targetElement').style.display === 'none' ? 'block' : 'none';
        });
    </script>
</div>
'''

# 主贴的模板
mainpostOfHtml = '''
<div class="my_post bangumi_container">
    <div class="bangumi_imgbox">
        <!-- 番剧图片 -->
        <img src="{BANGUMI_IMG}" class="bangumi_img" tittle="{BANGUMI_NAME}">
        <!-- 番剧信息 -->
        <ul class="bangumi_info">
            <li><span class="bangumi_tip">中文名: </span>{BANGUMI_CHINESE}</li>
            <li><span class="bangumi_tip">话数: </span>{BANGUMI_EPISODE}</li>
            <li><span class="bangumi_tip">放送开始: </span>{BANGUMI_DATE}</li>
            <li><span class="bangumi_tip">放送星期: </span>{BANGUMI_WEEKDAY}</li>
            <li><span class="bangumi_tip">评分: </span>{BANGUMI_SCORE}</li>
        </ul>
    </div>
    <div class="bangumi_content">
        <!-- 番剧标题链接  -->
        <a href="{BANGUMI_URL}" target="_blank" class="my_nameBox my_a">
            <h2>{BANGUMI_NAME}</h2>
        </a>
        <!-- 番剧介绍内容 -->
        <div class="my_content">
            <div class="my_p">
                {BANGUMI_CONTENT}
            </div>
            <div>
                <!-- 角色图片 -->
                {myPostImgs}
            </div>
        </div>
    </div>
</div>
'''

# 回贴的模板
repostOfHtml = '''
<div class="my_post">
    <div>
        <a href="{POST_USER_URL}" target="_blank" class="my_nameBox my_a">
            <img src="{POST_USER_IMG}" class="my_avatar" tittle="{POST_USER_NAME}" >
            <span class="my_name">{POST_USER_NAME}</span>
        </a>
    </div>
    <div class="my_content">
        <div class="my_p">
            {POST_CONTENT_P}
        </div>
        <div>
            {myPostImgs}
        </div>
    </div>
</div>
'''

# 角色图片的模板
imgOfHtml = '''
<img src="{BANGUMI_CHAR_IMG}" class="bangumi_char_img">
'''
