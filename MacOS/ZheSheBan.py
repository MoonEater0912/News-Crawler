#!/usr/bin/env python
# coding: utf-8

# 胡乱导入一些库
import requests
import bs4
import os
import datetime
import time
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import pandas as pd
import numpy as np

import tkinter as tk
from tkinter.filedialog import askdirectory

def crawlMain(keyword, maxpage):
    """
    爬取全国哲学社会科学工作办公室（哲社办）的主函数
    在用户输入关键词如”社会治理“后
    返回三个列表，分别按顺序包含标题、链接和概览
    存储在一个csv文件当中
    """

    # 初始化驱动
    options = webdriver.SafariOptions()
    driver = webdriver.Safari(options=options)
    
    # 初始化存储列表
    titlelst = []
    urllst = []
    abstractlst = []
    
    # 进行搜索
    fetchurl = "http://www.nopss.gov.cn" 
    driver.get(fetchurl)
    wait = WebDriverWait(driver, 10)  # 至多等待10s
    search_box = wait.until(EC.visibility_of_element_located((By.ID, 'keyword')))
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.ENTER)
    
    # 这个网站搜索后需要切换到新的标签页才能进入搜索结果页
    current_window_handle = driver.current_window_handle
    window_handles = driver.window_handles
    for handle in window_handles:
        if handle != current_window_handle:
            driver.switch_to.window(handle)
            break
    
    # 初始化当前页码
    curpage = 1

    # 循环爬取每一页
    while curpage <= maxpage:
        
        # 设置等待翻页区出现
        # 点击“下一页”后页面元素没有这么快刷新，会导致爬到的数据仍然是第1页的，因此加入了强制等待策略
        time.sleep(1) 
        wait = WebDriverWait(driver, 10)  # 至多等待10s
        temp = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'page_n')))    
        
        
        # 读取页面源代码
        text = driver.page_source
        
        # 解析页面源代码
        soup = bs4.BeautifulSoup(text, 'html.parser') 
        
        # 寻找到所有新闻条目
        content_zone = soup.find('div', class_='page2_list')
        contents = content_zone.find_all('li')
        
        # 遍历每个条目，读取其中的标题、url和概览
        for content in contents:
            
            # 寻找标题
            ttl = content.find('h2')
            ttla = content.find('a')
            title = ttla.text
            titlelst.append(title)
            
            # 寻找url
            urla = ttla.get('href')
            urllst.append(urla)
            
            # 寻找摘要
            # 万一没有摘要，设置了错误捕获
            try: 
                abstract = content.find('p')
                abstracta = abstract.text
                abstractlst.append(abstracta)
            except:
                abstractlst.append("【此条没有摘要！】")
            
        # 当前页爬取结束
        print("第{}页爬取成功！".format(curpage))
        
        # 寻找下一页按钮
        try:
            page_zone = driver.find_element(By.CLASS_NAME, 'page_n')
            time.sleep(1)
            page_buttons = page_zone.find_elements(By.TAG_NAME, 'a')
            next_button = page_buttons[-1]
            next_url = next_button.get_attribute('href')
            curpage = curpage + 1
            driver.get(next_url) # 直接用next_button.click()会失败，原因不明
        except:
            print("爬取过程在第{}页中断，可能因为设置爬取页数超过搜索结果页数".format(curpage))
            break
    
    # 循环结束，退出浏览器
    driver.quit()
    
    # 返回三个列表的列表
    return [titlelst, urllst, abstractlst]
        
        

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

df = pd.DataFrame()

df['Title'] = dt[0]
df['url link'] = dt[1]
df['Abstract'] = dt[2]

df_1 = df.drop_duplicates(subset='Title')

# 获取当前时间，用于生成保存文件名
curtime = datetime.datetime.now()
curtime = curtime.strftime("%Y%m%d%H%M%S")

# 生成文件名
savename = "ZSBGS_{}_{}.csv".format(keyword, curtime)
# df_1.to_csv("/Users/ollie/Desktop/{}.csv".format(savename))

# 唤出保存窗口
root = tk.Tk()
root.withdraw()
folder_path = askdirectory()

# 生成保存路径
savepath = folder_path + "/" + savename
try:
    df_1.to_csv(savepath)
    print(savename, ".csv 文件被储存于", folder_path)
except:
    print("保存文件时出错！")




