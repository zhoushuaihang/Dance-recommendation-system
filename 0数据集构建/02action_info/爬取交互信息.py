import csv
import random
import re
import time

import numpy as np
import pandas as pd
import requests

if __name__ == '__main__':

    headers = {
        'referer': 'https://www.bilibili.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
    }
    proxies = {
        "http": 'http://171.92.21.135:9000',
        "http": 'http://222.64.88.186:1088',
        "http": 'http://171.92.21.41:9000',
        "http": 'http://61.160.236.33:3129',
        "http": 'http://218.202.1.58	80',
        "http": 'http://223.247.140.229:30003',
        "http": 'http://220.133.119.75:3128',
        "http": 'http://218.204.153.156:8080',
        "http": 'http://61.182.213.83:7302',
        "http": 'http://58.240.110.171:8888',
        "http": 'http://183.247.152.98:53281',
        "http": 'http://180.121.134.77:8888',
        "http": 'http://221.122.91.76:9480',
        "http": 'http://39.130.150.23:80',
        "http": 'http://183.247.199.131:30001',
        "http": 'http://42.59.116.101:30001',
        "http": 'http://183.147.209.200:9000',
        "http": 'http://171.92.21.230:9000',
        "http": 'http://218.1.142.142:57114',
        "http": 'http://183.247.194.229:30001',
        "http": 'http://182.139.110.207:9000',
        "http": 'http://223.247.210.159:9002',
        "http": 'http://211.103.138.117:8000',
        "http": 'http://47.102.193.144:8891',
        "http": 'http://47.101.181.105:3128'
    }
    pn = 1
    # 排序种类 0是按时间排序 2是按热度排序
    sort = 2

    i = 1
    panduan = 0
    lable = 1
    data = pd.read_csv("dance.csv", encoding='utf-8')  # 读舞蹈信息文件
    file = open('action_info.csv', 'a', encoding='utf-8', newline='')#保存文件名
    # 先设置列名，并写入csv文件
    csv_writer = csv.DictWriter(file, fieldnames=["dance_id", "user_id", "lable"])
    csv_writer.writeheader()
    for num, da in enumerate(np.arange(0, len(data))):
        oid = data['id'][da]
        print(num)
        mid_set = set()
        for pn in range(pn):
            url = f'https://api.bilibili.com/x/v2/reply?pn={pn}&type=1&oid={oid}&sort={sort}'
            print(pn)
            try:
                reponse = requests.get(url, headers=headers, proxies=proxies)
                print(reponse.text)
                time.sleep(random.randint(10, 20))
                mid_data = re.findall('"mid":"(.*?)",', reponse.text)
                # mid_data1=re.findall('"mid":"(.*?)",',reponse.text)
                # print(mid_data)
                # break
                for mid in mid_data:
                    mid_set.add(mid)

                time.sleep(random.randint(5, 20))
                # print(mid_set)
            except Exception as e:
                print(e)
        print(mid_set)
        for m in mid_set:
            action_dict = {'dance_id': oid, 'user_id': m, 'lable': lable}
            # k取出key集合，average字典中key是时间，value是对应的值；
            key = list(action_dict.keys())
            # print(key)
            # 取出values集合,或者直接根据 字典的key值读取。
            value = list(action_dict.values())
            print(value)
            # time.sleep(random.randint(5, 20))
            csv_writer.writerow(action_dict)  # 数据写入csv文件

        print("第{}个舞蹈视频完成".format(num))
        # break
