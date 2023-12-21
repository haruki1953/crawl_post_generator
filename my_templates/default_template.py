# -*- coding: utf-8 -*-

# 整个html的模板，只有默认模板default_template.py包含
allOfHtml = '''
<!-- 通用css -->
<style type="text/css">
    .my_p {
        margin: 10px !important;
        color: black !important;
    }

    .my_thread {
        background-color: #f7f8fa;
        border-radius: 10px;
        margin: 10px 0;
        padding: 10px;
    }

    .my_nameBox {
        display: flex;
        align-items: center;
    }

    .my_name {
        margin: 10px;
    }

    .my_avatar {
        width: 44px;
        border-radius: 50%;
    }

    .my_a {
        /* text-decoration: none !important; */
        color: black !important;
    }

    .my_pic {
        /* width: 192px; */
        height: 108px;
        object-fit: cover;
        border-radius: 10px;
        margin: 3px;
    }

    .my_button {
        border-radius: 999em;
        padding: 0 10px;
    }

    .my_comments {
        padding-left: 30px;
    }

    .my_source {
        display: flex;
        justify-content: center;
        margin: 10px;
    }

    .my_post {
        margin: 24px 0;
    }
</style>
<!-- 自定义css -->
{myCustomCss}

<my-threads>
    {myThreads}
</my-threads>
'''

# 自定义css
customCssOfHtml = '''
<!-- default自定义css -->
'''

# 主题帖的模板
threadOfHtml = '''
<div class="my_thread">
    <div class="my_source">
        <a href="{THREAD_URL}" target="_blank" class="my_nameBox my_a">
            <img src="{SOURCE_IMG}" height="44px" tittle="{SOURCE_NAME}">
            <!-- <span class="my_name">{SOURCE_NAME}</span> -->
        </a>
    </div>
    {myMainPost}
    <button id="{TOGGLE_ID}_toggleButton" class="my_button">回帖 显示/隐藏</button>
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

# 回贴的模板，这里可以和主帖一样
repostOfHtml = mainpostOfHtml

# 每个图片的模板
imgOfHtml = '''
<img src="{POST_CONTENT_IMG}" class="my_pic">
'''
