import pandas as pd
#切分表
# 打开文件
# data=pd.read_csv("dance/dance1.csv",encoding='utf-8')#读舞蹈信息文件
data = pd.read_csv(r'dance.csv', "rb",encoding='utf-8',engine='python')
print(data.head())
print(data.iloc[0])
for i in range(0, 29):
    # print(i)
    # break
    save_data = data.iloc[i*1000 : (i+1)*1000-1]
    file_name = r"dance" + str(i) + '.csv'  # 保存文件路径以及文件名称
    save_data.to_csv("dance/"+file_name, index=False,encoding = 'utf_8_sig')  # 保存格式为.csv，如果是xlsx则修改为save_data.to_excel
print("success")