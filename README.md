# Tornado Demo
用Tornado做的一些项目练习，有的比较完整，是一整个项目，有的比较零星，只是在练习某些用法。

项目名后加了UI的，都是对原本的同名项目进行了完善和美化，相反，原本的项目会比较简陋，只是初期的版本。

## 目录
* [chatInWeb_UI](##chatInWeb_UI)
* [handwrittenDigitRecognition](##handwrittenDigitRecognition)
* [lotteryOnline_UI](##lotteryOnline_UI)
* [AsyncPractice](##AsyncPractice)
* [poemMakerPro](##poemMakerPro)
* [h5Practice](##h5Practice)
* [template_project](##template_project)

<a name="chatInWeb_UI"></a>
## chatInWeb_UI
**在线多人聊天系统**，数据不进数据库，记录在内存，HTML+CSS+JS+Tornado+Websocket

### 功能
- 用户名登录，由于没有用数据库，所以没有完善注册功能，密码验证也没有
- 用户id
- 创建聊天室
- 切换聊天室
- 退出聊天室
- 退出聊天室再加入时，能够恢复历史在线时间的聊天记录
- 同一聊天室多人聊天
- 聊天记录同步
- 显示时间
- 发送全局消息

<a name="handwrittenDigitRecognition"></a>
## handwrittenDigitRecognition
**Web端手写数字识别系统**，在浏览器使用鼠标或者手写数字，发送到后端用Tensorflow训练的模型识别

HTML+CSS+JS+Canvas+Tornado+Websocket+Tensorflow+LeNet-5模型

<a name="lotteryOnline_UI"></a>
## lotteryOnline_UI
**活动抽奖网页版程序**，同样数据只记录在内存，HTML+CSS+JS+Tornado+Numpy

### 功能
- 设置奖品数量
- 上传抽奖人员名单
- 手动输入测试名单
- 随机抽奖，按概率中奖
- 分批抽奖，每次默认5人

<a name="AsyncPractice"></a>
## AsyncPractice
**同步异步的练习**，主要是熟悉Tornado异步的原理和三种实现方法
具体可以看我的博客[Python中的异步](https://catchdream.me/2019/03/17/Python%E4%B8%AD%E7%9A%84%E5%BC%82%E6%AD%A5/)和[Tornado中的异步](https://catchdream.me/2019/03/17/Tornado%E4%B8%AD%E7%9A%84%E5%BC%82%E6%AD%A5/)

<a name="poemMakerPro"></a>
## poemMakerPro
**Tornado中文文档中的练习**，主要涉及表单上传和变量的使用

<a name="h5Practice"></a>
## h5Practice
**结合H5的小练习**，内容并不多

<a name="template_project"></a>
## template_project
**每次做项目的模板**，如果是Tornado的相关项目，可以直接download后修改路由和config端口

static目录下的js/, css/, html/,这三个目录按需求自己创建

