### 一个爬取中国主流新闻网站的桌面爬虫应用
- 适用于MacOS，因为使用了Safari webdriver
- main函数中构建GUI界面，其余各个.py文件用于爬取文件名所指新闻平台
- 用户在应用中可以指定目标平台、检索关键词和迭代次数（即爬取页数）
- 爬取结果中标题重复的条目会被去重
- 目前已经实现的网站可以在main.py的字典中看到

#### 效果图

<img width="337" alt="截屏2024-03-26 16 38 48" src="https://github.com/MoonEater0912/News-Crawler/assets/159446897/f84ff8c4-e14e-438d-8cb7-b33f072cca88">

<img width="342" alt="截屏2024-03-26 16 42 09" src="https://github.com/MoonEater0912/News-Crawler/assets/159446897/f42e4224-de0c-4d03-8adb-b6119015fae2">



### 一个需要用户输入链接的讲座信息整理脚本
- 这是一个单独的脚本
- 适用于“学术讲座”和“北大清华讲座”两个公众号，可能也适合其他类似的公众号
- 将任意一篇聚合讲座信息的链接复制，例如https://mp.weixin.qq.com/s/yNJmKaV0Bwfqb0ElYRXTwQ ，然后运行该脚本，粘贴链接
- 输出是一个csv文件，包括讲座名称、时间、主讲和观看方式，可以选择保存路径
