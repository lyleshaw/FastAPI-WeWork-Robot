# FastAPI-WeWork-Robot

> 基于FastAPI创建的、使用企业微信交互的机器人系统

## 起因

我从去年想要拥有一个TODOlist开始，一步步的拓展这个想法：从单纯的列出任务，到任务到期提醒...一点点的有其他新的想法。

关于推送方式，我最早是希望通过发送邮件，然后通过微信企业邮的邮件提醒达到推送效果，而后发现了server酱，又开始使用这种方式实现微信推送，期间又接触了某个可以白嫖的短信api，但是免费一个帐号大概400条（配置还很麻烦），最终因为学校的企业微信最近推送了好几条消息...意识到企业微信是目前最适合的推送方式。

当然，单纯了做了任务提醒的功能后，发现企业微信的api还挺好玩的，于是一点点看文档写了其他一些小功能（参考func.py文件）

## 配置及使用

> requirements：fastapi,uvicorn

### 企业微信配置

首先，请配置config.py文件按要求填写：

```
# sToken和sEncodingAESKey来自于企业微信创建的应用
# sCorpID为企业微信号

sToken = ""
sEncodingAESKey = ""
sCorpID = ""
```

### 中间件配置

如果想手动设置中间件（默认为不限制访问），请参考FastAPI文档设置main.py文件中的如下代码

```
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 使用

请先启动main.py程序

然后按照[企业微信的要求](https://work.weixin.qq.com/api/doc/90001/90143/91116)完成URL验证。

而后即可正常使用。

## 自定义功能

如果您需要自定义企业微信被动回复功能，可以对func.py文件中的handle_msg函数进行修改。

handle_msg有两个参数

+ to_user_id: str # 用户名
+ recived_msg: str # 用户发送的信息

返回值即为被动回复的消息内容

## 反馈&联系我

本项目基于[企业微信官方python库](https://github.com/sbzhu/weworkapi_python)进行修改。

如果有其他问题，可以通过如下方式联系我

+ [lyle@hdu.edu.cn](mailto:lyle@hdu.edu.cn)
+ [lyleshaw.com](https://lyleshaw.com/)