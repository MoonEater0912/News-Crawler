#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import bs4
import os
import datetime
import time
import argparse


# In[39]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# In[48]:


import pandas as pd
import numpy as np


# In[44]:


def crawlMain(keyword, maxpage):
    """
    爬取人民网的主函数
    在用户输入关键词如”社会治理“后
    返回三个列表，分别按顺序包含标题、链接和概览
    存储在一个csv文件当中
    """

    # 初始化驱动
    driver = webdriver.Safari()
    
    # 初始化存储列表
    titlelst = []
    urllst = []
    abstractlst = []
    
    # 进行搜索
    fetchurl = "http://search.people.cn"
    driver.get(fetchurl)
    wait = WebDriverWait(driver, 5)
    search_box = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.ENTER)
    
    # 初始化当前页码
    curpage = 1
    
    # 循环爬取每一页
    while curpage <= maxpage:
        
        time.sleep(3)
        
        # 读取页面源代码
        text = driver.page_source
        
        # 解析页面源代码
        soup = bs4.BeautifulSoup(text, 'html.parser') 
        
        # 寻找到所有新闻条目
        contents = soup.find_all('div', class_='content')
        
        # 遍历每个条目，读取其中的标题、url和概览
        for content in contents:
            
            # 寻找标题
            ttl = content.find('div', class_='ttl')
            ttla = ttl.find('a')
            title = ttla.text
            titlelst.append(title)
            
            # 寻找url
            urla = ttla.get('href')
            urllst.append(urla)
            
            # 寻找摘要
            abstract = content.find('div', class_='abs')
            abstracta = abstract.text
            abstractlst.append(abstracta)
            
        # 当前页爬取结束
        print("当前第{}页爬取结束！".format(curpage))
        
        # 寻找下一页按钮
        next_page_button = driver.find_element(By.CLASS_NAME, 'page-next')
        curpage = curpage + 1
        next_page_button.click()
    
    # 循环结束，退出浏览器
    driver.quit()
    
    # 返回三个列表的列表
    return [titlelst, urllst, abstractlst]
        
        
            
            
        
    


# In[45]:

# 接受父进程传入的参数
# 创建参数解析器
parser = argparse.ArgumentParser()
parser.add_argument("--keyword", help="关键字参数")
parser.add_argument("--maxpage", type=int, help="最大页数参数")
args = parser.parse_args()

# 将关键字参数和最大页数参数存储在变量中
keyword = args.keyword
maxpage = args.maxpage

dt = crawlMain(keyword, maxpage)


# In[55]:


df = pd.DataFrame()


# In[57]:


df['Title'] = dt[0]
df['url link'] = dt[1]
df['Abstract'] = dt[2]


# In[59]:


df_1 = df.drop_duplicates(subset='Title')


# In[ ]:





# In[65]:


df_1.to_csv("/Users/ollie/Desktop/人民网-社会治理.csv")


# In[ ]:




