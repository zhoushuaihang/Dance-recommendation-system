# -*-coding:utf-8-*-
import numpy as np
import pandas as pd
import requests
import json
import csv
import time
import random
import pprint
def get_response(html_url):
    header ={
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'

                   }
    resource=requests.get(url=html_url,headers=header)
    return  resource
if __name__ == '__main__':
    data=pd.read_csv("user_set0.csv")
    file = open('user_info0.csv', 'a', encoding='utf-8', newline='')
    # 先设置列名，并写入csv文件
    csv_writer = csv.DictWriter(file, fieldnames=['id', 'birthday', 'level', 'name', 'sex', 'school', 'sign'])
    csv_writer.writeheader()
    for num,da in enumerate(np.arange(0,len(data))):
        try:

            id=data['user_id'][da]
            url='https://api.bilibili.com/x/space/acc/info?mid={}&token=&platform=web&jsonp=jsonp'.format(id)
            html_url=get_response(url)
            time.sleep(random.randint(1, 5))
            html_json = json.loads(html_url.text)
            json_list = html_json.get('data')
            # pprint.pprint(type(json_list))
            id=json_list.get('mid')
            birthday=json_list.get('birthday')
            level = json_list.get('level')
            name=json_list.get('name')
            sex=json_list.get('sex')
            school=json_list.get('school').get('name')
            sign=json_list.get('sign')
            info = {"id": id, "birthday" : birthday, "level" : level, "name" : name, "sex" : sex, "school" : school, "sign" : sign}
            # k取出key集合，average字典中key是时间，value是对应的值；
            key = list(info.keys())
            # 取出values集合,或者直接根据 字典的key值读取。
            value = list(info.values())
            csv_writer.writerow(info)  # 数据写入csv文件
            time.sleep(random.randint(1,10))
            print("第{}位用户:{}信息采集成功！！！".format(num,id))
        except Exception as e:
            print(e)
            print("第{}位用户:{}信息采集失敗！！！".format(num,id))
            continue



    file.close()
