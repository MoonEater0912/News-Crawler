#!/usr/bin/env python
# coding: utf-8

# 导入必要的库
import pandas as pd
import requests
import re
import tkinter as tk
from tkinter import filedialog

# 用户输入讲座信息聚合页链接
url = input()
response = requests.get(url)
content = response.text

# 先爬取主题
pattern = r'【主题】([^<]+)'
topics = re.findall(pattern, content)



# 然后爬取时间
times = []

for topic in topics:
    validindex = content.find("【主题")
    pattern = r'【时间】([^<]+)'
    validcontent = content[validindex:]
    index = validcontent.find(topic)
    times.append(re.search(pattern, validcontent[index:]).group(1))
    

# 然后爬取主讲人
teachers = []

for topic in topics:
    validindex = content.find("【主题")
    pattern = r'【主讲】([^<]+)|【嘉宾】([^<]+)'
    validcontent = content[validindex:]
    index = validcontent.find(topic)
    groups = [re.search(pattern, validcontent[index:]).group(i) for i in [1,2]]
    v_groups = [i for i in groups if i is not None]
    try:
        teachers.append(v_groups[0])
    except:
        teachers.append("此条主讲人信息无法获取！")
    

# 然后爬取观看方式
views = []

for topic in topics:
    validindex = content.find("【主题")
    pattern = r'【观看方式】([^<]+)|【观看地点】([^<]+)|【地点】([^<]+)|【线上观看】([^<]+)'
    validcontent = content[validindex:]
    index = validcontent.find(topic)
    groups = [re.search(pattern, validcontent[index:]).group(i) for i in [1,2,3,4]]
    v_groups = [i for i in groups if i is not None]
    try:
        views.append(v_groups[0])
    except:
        views.append("此条观看方式无法获取！")
    

# 整合到一个数据框中
df = pd.DataFrame([])
df['topic'] = topics
df['time'] = times
df['teacher'] = teachers
df['view'] = views


# 接下来对爬取结果进行保存
root = tk.Tk()
root.withdraw()

file_path = filedialog.asksaveasfilename(defaultextension='.csv',
                                         filetypes=[('CSV Files', '*.csv')])
if file_path:
    df.to_csv(file_path, index=False)
    print("文件保存成功，路径为：{}".format(file_path))
else:
    print("用户取消保存！")

root.destroy()







