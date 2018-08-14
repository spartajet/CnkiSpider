__author__ = 'Xiaozhong GUO'
from configparser import ConfigParser
import urllib
from urllib.parse import quote
from urllib import request
from bs4 import BeautifulSoup
import math
import logging
import socket
import list_paper_operate
import pymysql

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("log.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(console)
    cf = ConfigParser()
    cf.read("cnki.conf", encoding='utf-8')
    keyword = cf.get('cnki', 'keyword')  # 关键词
    category = cf.get('cnki', 'category')
    # max_page = cf.getint('cnki', 'max_page')  # 最大页码
    search_location = cf.get('cnki', 'search_location')  # 搜索位置
    current_page = cf.getint('cnki', 'current_page')

    # 构造不同条件的关键词搜索
    keywords_values = {
        '全文': 'qw',
        '主题': 'theme',
        '篇名': 'title',
        '作者': 'author',
        '摘要': 'abstract'
    }

    category_values = {
        '全部': '',
        '学术期刊': 'CJFDTOTAL',
        '博士论文': 'CDFDTOTAL',
        '硕士论文': 'CMFDTOTAL',
        '会议论文': 'CPFDTOTAL'
    }

    # keyword_val = str(keywords_values[search_location]) + ':' + str(keyword)

    keyword_val = str(keyword)
    category_val = str(category_values[category])
    # index_url = 'http://search.cnki.com.cn/Search.aspx?q=' + quote(
    #     keyword_val) + '&rank=zyk&cluster=&val=&p='  # quote方法把汉字转换为encodeuri?
    index_url = 'http://search.cnki.com.cn/search.aspx?q={}&rank=relevant&cluster=zyk&val={}&p='.format(
        quote(keyword_val),
        category_val)

    logger.info('search url is {}'.format(index_url))

    # 获取最大页数
    html = request.urlopen(index_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    page_sum_text = soup.find('span', class_='page-sum').get_text()
    max_page = int(math.ceil(int(page_sum_text[7:-1]) / 15))
    logger.info('max page is {}'.format(max_page))
    cf = ConfigParser()
    cf.read("cnki.conf", encoding='utf-8')
    cf.set('cnki', 'max_page', str(max_page))
    cf.write(open('cnki.conf', 'w', encoding='utf-8'))

    # 打开数据库连接
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='gear_paper', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO paper(title, url, year,authors," \
          "keywords,abstract,publisher,cite,download," \
          "unit,reference,category) " \
          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

    # sql = "INSERT INTO paper(abstract, authors, category,cite," \
    #       "download,keywords,publisher,reference,title," \
    #       "unit,url,year) " \
    #       "VALUES (%s,%s,%s,%d,%d,%s,%s,%d,%s,%s,%s,%d)"

    for i in range(current_page, max_page):
        page_num = 15
        page_str_num = i * page_num
        page_url = index_url + str(page_str_num)
        logger.info('current search page: {}'.format(page_url))
        attempts = 0
        success = False
        while attempts<50 and not success:
            try:
                papers = list_paper_operate.operate_list_paper(page_url, category)

                socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                success = True
            except socket.error:
                attempts += 1
                print("Start第" + str(attempts) + "次重试！！")
                if attempts == 50:
                    break
            except urllib.error:
                attempts += 1
                print("Start第" + str(attempts) + "次重试！！")
                if attempts == 50:
                    break
        try:
            paper_objects = []
            for paper in papers:
                paper_objects.append((paper.title, paper.url, paper.year, paper.authors, paper.keywords, paper.abstract,
                                      paper.publisher, paper.cite, paper.download, paper.unit, paper.reference,
                                      paper.category))
            cursor.executemany(sql, paper_objects)
            cf.set('cnki', 'current_page', str(i))
            cf.write(open("cnki.conf", "w", encoding='utf-8'))
        except Exception as e:
            db.rollback()
            print("执行MySQL: %s 时出错：%s" % (sql, e))
        db.commit()
    # spider_paper.spider_paper()  # spider_paper补全文章信息
    cursor.close()
    db.close()
    logger.info('spider end!!!')
