# -*-coding:utf-8-*-
# 爬取B站中国舞视频20210901-20210930时间段视频
import requests
import re
import json
import csv
import random
import time
import pymysql


def save_sql(dmdic):
    conn = pymysql.connect(host='', user='root', passwd='', port=3306, db='',
                           charset='utf8mb4')
    cursor = conn.cursor()
    data = dmdic
    table = 'dance-info'
    keys = ', '.join(data.keys())
    print(keys)
    values = ', '.join(['%s'] * len(data))
    # values = ", ".join(data.values())
    # print(values)

    values = ', '.join(['%s'] * len(data))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    cursor.execute(sql, tuple(data.values()))
    print("Successful")
    conn.commit()
    try:
        if cursor.execute(sql, tuple(data.values())):
            print("Successful")
            conn.commit()
    except Exception as e:
        print('Failed', e)
        # filed_list.append(data)
        # print(data)
        conn.rollback()
    conn.close()

def get_response(html_url):
    header ={
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
        'referer': 'https://www.bilibili.com/',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'cookie': "buvid3=61574299-9729-4963-68D3-3B5A15FAB89024853infoc; _uuid=1A273A3B-610D3-3F94-D147-3794FA5EAAD924581infoc; buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO8616567586392809; blackside_state=0; rpdid=|(k|uJ)l|R|)0J'uYlY~l)Yl); hit-dyn-v2=1; nostalgia_conf=-1; DedeUserID=281005551; DedeUserID__ckMd5=5e45c9ed58771aa7; b_ut=5; b_nut=100; is-2022-channel=1; SESSDATA=6641288b%2C1681180073%2C0284d%2Aa1; bili_jct=c4b52bacd305d71fcd22ec999ddefd79; sid=60z0o5k0; bsource=search_baidu; fingerprint3=c482a3580f87f3bee7ae2fdc4ba98d61; fingerprint=74a3bc39e9b1ced7dd97e38946f7043a; bp_video_offset_281005551=716448760464408600; CURRENT_QUALITY=112; buvid4=66A8D5AA-1946-7ABD-3A22-A318F6322E3A14409-022040413-OswTBaywvfsOTmM%2BQSle%2BQ%3D%3D; buvid_fp=74a3bc39e9b1ced7dd97e38946f7043a; i-wanna-go-back=-1; b_lsid=3710B6102F_183D404FF7D; innersign=0; PVID=1; CURRENT_FNVAL=16",
        'origin':"'https://www.bilibili.com'"
                   }
    resource=requests.get(url=html_url,headers=header)
    return  resource

def get_video_info(html_url):
    """
    获取视频标题/CID/SESSION
    """
    response=get_response(html_url)
    cid=re.findall('"cid":(\d+),',response.text)[0]
    session=re.findall('"session":"(.*?)"',response.text)[0]
    title=re.findall('<h1 title="(.*?)" class="video-title tit">',response.text)[0].replace(' ','')
    desc_info=re.findall('<span class="desc-info-text">([\s\S]*?)</span>',response.text)[0]
    print(cid,session,title,desc_info)

    # print(response.text)

if __name__ == '__main__':
        page=143
        file = open('dance2.csv', 'a', encoding='utf-8', newline='')#保存文件名
        # 先设置列名，并写入csv文件
        csv_writer = csv.DictWriter(file, fieldnames=["id","title","tag","description","author","bvid","arcurl","favorites","pic","play","pubdate"] )
        csv_writer.writeheader()

        for p in range(2):
            p=p+page
            url="https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&copy_right=-1&new_web_tag=1&order=click&cate_id=200&page={}&pagesize=30&time_from=20210901&time_to=20210930".format(p)
            # print(url)
            html_url=get_response(url)
            if html_url.status_code == 200:
                time.sleep(random.randint(1, 5))
            else:
                continue
            html_json=json.loads(html_url.text)
            json_list=html_json.get('result')
            try :
                for n,i in enumerate(json_list):
                    id = i.get("id")
                    title = i.get("title")
                    tag = i.get("tag")
                    description =i.get("description")
                    author = i.get("author")
                    bvid = i.get("bvid")
                    arcurl = i.get("arcurl")
                    favorites = i.get("favorites")
                    pic = i.get("pic")
                    play = i.get("play")
                    pubdate = i.get("pubdate")
                    info={"id":id,"title":title,"tag":tag,"description":description,"author":author,"bvid":bvid,"arcurl":arcurl,"favorites":favorites,"pic":pic,"play":play,"pubdate":pubdate
                           }
                    print(info)
                    time.sleep(random.randint(1, 5))
                    # k取出key集合，average字典中key是时间，value是对应的值；
                    key = list(info.keys())
                    # 取出values集合,或者直接根据 字典的key值读取。
                    value = list(info.values())
                    csv_writer.writerow(info)  # 数据写入csv文件
                    print("完成：  {}页的第{}个： {}    ！写入。。".format(p,n,title))
                    time.sleep(random.randint(1, 3))
            except Exception as e:
                print(e)
            time.sleep(random.randint(5,10))
        print("恭喜！！！写入完成！！！")
        #  # 关闭文件夹
        file.close()