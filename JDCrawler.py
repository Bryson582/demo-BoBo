#导入必要的包
import requests
import json
import time as tm
import pandas as pd
# header这个的作用在于伪装成浏览器进行操作，有些网页识别到不是浏览器就不能访问，User-Agent能伪装
# User-Agent一般在刚刚找网页网址url的Headers的下面就有
#      我们可以简单的解析这个网址，前面不动，后面的我们点击下一页，看会出现什么改变
#      https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=5225346&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1
#      我们发现只有page在变化，根据这个我们可以进行翻页爬取，我们先进行第一页的操作
#      先向浏览器发送请求
header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
              "Cookie":"shshshfpb=xj4lLl1SPSope8KtAoRC1dA%3D%3D; shshshfpa=4206b744-99d6-2cbd-d1ab-5e78d2f9260e-1607941670; __jdu=16111263892761261467547; __jdv=76161171|www.google.com|-|referral|-|1617264490100; user-key=827c8c8e-e7b5-488e-8b93-a909cb64fb75; cn=0; pinId=6o1UzLtj4GAXnBRFNNc5brV9-x-f3wj7; pin=jd_6738cd22452f4; unick=jd_6738cd22452f4; _tp=FymwWoj%2BKYiAhvcU%2FYi70CaPAUdAAv7Q8cJk6b1G6Zs%3D; _pst=jd_6738cd22452f4; TrackID=1t1HczUHXzWHBws9A34zg_9OShlAhGYZSTcmktlmk1dMi3DJhzX_od7Y3frRpnGeO3fVJfSWjWIT-ZtEmj4h0YJNRNRRJsc3O4SYNFfg3xtlYGZbRlJSeus6ydWvW4qBV; PCSYCityID=CN_210000_210200_210213; jwotest_product=99; areaId=8; ipLoc-djd=8-573-46824-0; __jdc=122270672; shshshfp=097e77af59a00eecd110c7c35c134713; __jda=122270672.16111263892761261467547.1611126389.1618184022.1618213498.27; shshshsID=cc51dd42606f34422ccd5f42ad7f710b_2_1618213535214; __jdb=122270672.2.16111263892761261467547|27.1618213498; JSESSIONID=891956B0ECEC510A3DC72B6BF51EA0BF.s1; 3AB9D23F7A4B3C9B=4LCQKOFGP572KUKDZ4TGMUMECYIMPBTLHR2AR4N6SLH2PEFUSR4PU7G3RPNHUCQRE75LDD7FR23MKJ6AH2PVHQBL3M"
          }
buyer_id = []
nickname = []
content = []
score = []
time = []
for page in range(0, 100):
     #for循环爬取不同的页面
     #此处的url需要使用我们在网页开发者工具中找到评论对应的Request URL
     url = "https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98&productId=100019867468&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1".format(page)
     response = requests.get(url, headers=header)
     data = response.text
     # 下面的解析json.load是我们需要进行解码
     # json.loads 用于解码 JSON 数据。该函数返回 Python 字段的数据类型。
     # 下面的写法有时候会出现错误 也可以直接使用字符串分割更为方便
     # 例如 jd = json.loads(data[m:-1])
     # 其中m的数值需要根据response中json而定
     jd = json.loads(data.lstrip('fetchJSON_comment98(').rstrip(');'))
     # data_list = jd['comments']
     print(jd)
     print(jd['comments'])
     print(page)
     for data in jd['comments']:
          buyer_id.append(data['id'])
          nickname.append(data['nickname'])
          content.append(data['content'])
          score.append(data['score'])
          time.append(data['creationTime'])
     # tm.sleep(1)
data_frame = pd.DataFrame({'buyer_id':buyer_id,'nickname':nickname,'content':content,'score':score,'time':time})
data_frame.to_csv('小米手环6代NFC版本100019867468.csv',index=False,sep=',')
