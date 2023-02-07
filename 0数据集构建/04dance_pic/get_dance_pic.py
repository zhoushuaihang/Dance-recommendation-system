# -*-coding:utf-8-*-
import numpy as np
import pandas as pd
import requests
import time
import random
def get_response(html_url):
    header ={
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
        }
    resource=requests.get(url=html_url,headers=header)
    return  resource
if __name__ == '__main__':
    data=pd.read_csv('dance-info(0801-1231).csv',encoding='utf-8')
    for da in np.arange(len(data)):
        id=data['id'][da]
        pic=data['pic'][da]
        # print(id)
        # print("获取第{}个视频封面！！".format(da))
        url = "http:{}".format(pic)
        html_url=get_response(url)
        html_content=html_url.content
        with open(f"dancep/{id}" + '.jpg', mode='wb') as f:
            f.write(html_content)
            print('第{}/{}个视频封面写入成功！！'.format(da,len(data)))




