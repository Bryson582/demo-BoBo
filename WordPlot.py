# 词云图
import matplotlib.pyplot as plt  # 数学绘图库
from PIL import Image
import numpy as np  # 科学数值计算包，可用来存储和处理大型矩阵
import jieba  # 分词库
from wordcloud import WordCloud, ImageColorGenerator  # 词云库
import pandas as pd


stopwords_path = '/Users/brycelee/Documents/GitHub/stopwords/baidu_stopwords.txt' # 停用词词表

# 我们此处为了关注用户在实际评论当中的所使用的词语 去除掉了停用词
# 但是对于我们研究的问题来说 诸如小米 手环等词语来说并没有研究的价值和意义
# 所以我们把小米和手环也作为停用词添加到我们的停用词词表中

# 停用词函数

def jiebaclearText(text):
    mywordlist = []
    # jieba分词
    # 详情可见:https://github.com/fxsjy/jieba
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)
    f_stop = open(stopwords_path)
    try:
        f_stop_text = f_stop.read()
    finally:
        f_stop.close()
    f_stop_seg_list = f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ''.join(mywordlist)

df = pd.read_csv('./小米手环5代.csv')

#这里生成词云图之前 我们是需要将所有的评论内容都合成字符串
text = " ".join([str(elem) for elem in df['content'].tolist()])
text = jiebaclearText(text)


cut_text = jieba.cut(text, cut_all=False)
result = "/".join(cut_text)  # 必须给个符号分隔开分词结果,否则不能绘制词云

# 自定义图片路径
image = Image.open('demo.jpeg')
graph = np.array(image)

# 4、产生词云图
# 有自定义背景图：生成词云图由自定义背景图像素大小决定
# 此处也可以进行颜色变换 生成不依照图片原本颜色的词云图
wc = WordCloud(font_path="WeiRuanYaHei-1.ttf", background_color='white', max_font_size=100,
               mask=graph)
wc.generate(result)

# 5、绘制文字的颜色以背景图颜色为参考
image_color = ImageColorGenerator(graph)  # 从背景图片生成颜色值
wc.recolor(color_func=image_color)
wc.to_file("小米手环5代词云图.png")  # 按照背景图大小保存绘制好的词云图，比下面程序显示更清晰

# 6、显示图片
plt.figure("词云图")  # 指定所绘图名称
plt.imshow(wc)  # 以图片的形式显示词云
plt.axis("off")  # 关闭图像坐标系
plt.show()
