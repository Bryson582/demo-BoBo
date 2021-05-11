import pandas as pd
import time
from aip import AipNlp
import jieba
from os import path
import jieba.analyse as analyse
import threading

d = path.dirname(__file__)
# 下载停用词词表 https://github.com/goto456/stopwords
stopwords_path = '/Users/brycelee/Documents/GitHub/stopwords/baidu_stopwords.txt' # 停用词词表

#下面对于线程类的重写我们进行函数并发时可以使用
# class MyThread(threading.Thread):
#     def __init__(self, func, args=()):
#         super(MyThread, self).__init__()
#         self.func = func
#         self.args = args
#
#     def run(self):
#         self.result = self.func(*self.args)
#
#     def get_result(self):
#         try:
#             return self.result
#         except Exception:
#             return None


#去除停用词
def jiebaclearText(text):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)
    f_stop = open(stopwords_path)
    try:
        f_stop_text = f_stop.read()
        # f_stop_text = (f_stop_text, 'utf-8')
    finally:
        f_stop.close()
    f_stop_seg_list = f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ''.join(mywordlist)

#TF_IDF计算词频
def countIDF(text, topK):
    tfidf = analyse.extract_tags
    keywords = tfidf(text, topK, withWeight=True)
    print(keywords)

    keywords = dict(keywords)
    # 我们这里可以把keywords列表变成字典
    # 然后把词语和权重分离到两个列表当中
    # print(keywords)
    list1 = []
    list2 = []
    for i in keywords.keys():
        list1.append(i)
    for j in keywords.values():
        list2.append(j)
    return [list1,list2]

#百度AI开放平台的AK和SK
""" 你的 APPID AK SK """
APP_ID = '*****'
API_KEY = '******'
SECRET_KEY = '******'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

def sent(i):
    sC = client.sentimentClassify(i)
    print(sC['items'][0]['sentiment'])
    print(sC['items'][0]['confidence'])
    sen1.append(sC['items'][0]['sentiment'])
    sen2.append(sC['items'][0]['confidence'])

# def remark(i,options):
#     cT = client.commentTag(i, options)
#     print(cT['items'][0]['prop'])
#     print(cT['items'][0]['adj'])
#     sen3.append(cT['items'][0]['prop'] + cT['items'][0]['adj'])


if __name__ == '__main__':
     df = pd.read_csv('./小米手环5代.csv')
     print(df['content'])
     # 我想在这里使用一下SDK 这样处理起来会更加的方便
     # 我们先使用情感分析 输入内容看一下
     sen1 = []
     sen2 = []
     for i in df['content']:
          print(i)
          """
          情感倾向分析
          """
          try:
            sent(i)
          except Exception as e:
              print("情感接口识别失败")
              sen1.append(" ")
               sen2.append(" ")
     """
     词频分析 TF-IDF
     """
     # 首先进行词频分析的时候 我们需要首先对文本做一定程度的预处理
     # 我们首先要去除停用词
     # 去除停用词之后有一点我们需要注意的 我上次在使用TF-IDF的时候
     # 我是先把数据按照关键词分类 所以说同一个主题的笔记内容都在一个for循环里
     # 对于这项评论来说 我们可以认为都是在一个主题下的 所以说我们需要把所有的笔记都变成一个长字符串然后放到函数中

     # 我们把list先变成string

     str1 = " ".join([str(elem) for elem in df['content'].tolist()])
     # 接下来调用函数做词频分析
     str1 = jiebaclearText(str1)
     ans = countIDF(str1, 100)
     print(ans[0])
     print(ans[1])

     """
     接下来我们可以先把结果写回到本地文件
     """
     result = pd.DataFrame({"内容":df['content'],"倾向":sen1,"倾向置信区间":sen2})
     # 这里面因为TFIDF的结果不是和每一行一一对应的 我们是把所有的评论内容放到一起进行操作的 所以说我们这个时候需要把该结果放到另一张表中
     tfIDF = pd.DataFrame({"关键词":ans[0],"权重":ans[1]})
     result.to_csv("小米手环六五代情感倾向分析.csv",sep=",",index=False)
     tfIDF.to_csv("demo.csv",sep=",",index=False)
