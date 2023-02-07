# -*-coding:utf-8-*-
import requests
import re
import pprint
import json
import subprocess
import os
import pandas as pd
import csv
import numpy as np
import random
import time



headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'referer': 'https://www.bilibili.com/',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
}
proxyHost = ""
proxyPort = ""
proxyUser = ""
proxyPass = ""
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

# 设置 http和https访问都是用HTTP代理
proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}
if __name__ == '__main__':
    data=pd.read_csv("dance_info(0801-1231).csv",encoding='utf-8')#读舞蹈信息文件

    # for num,da in enumerate(np.arange(0,len(data))):

    for num, da in enumerate(np.arange(len(data))):
        bv=data['bvid'][da]
        id=data['id'][da]
        url='https://www.bilibili.com/video/{}/'.format(bv)
        html = requests.get(url, headers=headers)
        # html=requests.get(url=url,headers=headers,proxies=proxies)
        # html = requests.get(url=url, headers=headers, proxies=proxies)
        title=re.findall('<h1 title="(.*?)"',html.text)[0]
        title=re.sub(r'[\/:*?"<>|]','',title)
        html_data=re.findall('<script>window.__playinfo__=(.*?)</script>',html.text)[0]
        json_data=json.loads(html_data)
        print(title)
        # print(html_data)
        # pprint.pprint(json_data)
        audio_url=json_data['data']['dash']['audio'][0]['baseUrl']
        # print(audio_url)
        video_url=json_data['data']['dash']['video'][0]['baseUrl']
        # print(video_url)
        time.sleep(random.randint(1, 30))
        audio_content=requests.get(url=audio_url,headers=headers).content#获取二进制数据
        time.sleep(random.randint(1, 30))
        video_content=requests.get(url=video_url,headers=headers).content
        with open(f"{title}"+'.mp3',mode='wb') as f:
            f.write(audio_content)
        with open(f"{title}"+'.mp4',mode='wb') as f:
            f.write(video_content)
        print("保存成功！！")

        # //-vcodec copy ：视频只拷贝，不编解码
        # //-acodec copy : 音频只拷贝，不编解码
        # //new.mp4 ：新生成的文件，文件的长度由两个输入文件的最长的决定
        # cmd=f"ffmpeg -i BV188411W7rj.mp4 -i BV188411W7rj.mp3 -vcodec copy -acodec copy {title}.mp4"
        cmd = f"ffmpeg -i {title}.mp4 -i {title}.mp3 -c:v copy -c:a aac -strict experimental {id}.mp4"

        subprocess.run(cmd,shell=True)
        print(title,'视频合成完成')

        os.remove(f'{title}.mp4')
        os.remove(f'{title}.mp3')
        print("第{}/{}个成功!!!".format(num,len(data)))


