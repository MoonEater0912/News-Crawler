#### 一个爬取中国主流新闻网站的桌面爬虫应用
- 需求来自某研究院离谱RA工作
- main函数中构建GUI界面，其余各个.py文件用于爬取文件名所指新闻平台
- 用户在应用中可以指定目标平台、检索关键词和迭代次数（即爬取页数）
- 爬取结果中标题重复的条目会被去重
- 目前只实现了人民网（http://www.people.com.cn）