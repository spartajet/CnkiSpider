__author__ = 'Xiaozhong GUO'
import urllib
from bs4 import BeautifulSoup
import socket


class Paper(object):

    def __init__(self, url, year, title, authors, keywords, abstract, publisher, cite, download, unit, reference,
                 category):
        self.url = url
        self.year = year
        self.title = title
        self.authors = authors
        self.keywords = keywords
        self.abstract = abstract
        self.publisher = publisher
        self.cite = cite
        self.download = download
        self.unit = unit
        self.reference = reference
        self.category = category


def create_paper(url, category, title, publisher, year, download, cite):
    temp_paper = Paper(url, year, title, '', '', '', publisher, cite, download, '', '', category)
    attempts = 0
    success = False
    while attempts<50 and not success:
        try:
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            socket.setdefaulttimeout(10)  # 设置10秒后连接超时
            success = True
        except socket.error:
            attempts += 1
            print("Paper第" + str(attempts) + "次重试！！")
            if attempts == 50:
                return
        except urllib.error:
            attempts += 1
            print("Paper第" + str(attempts) + "次重试！！")
            if attempts == 50:
                return
    title = soup.find_all('div',
                          style="text-align:center; width:740px; font-size: 28px;color: #0000a0; font-weight:bold; font-family:'宋体';")
    abstract_div = soup.find_all('div', style='text-align:left;word-break:break-all')
    author_div = soup.find_all('div', style='text-align:center; width:740px; height:30px;')
    author = ''
    # 获取作者名字
    for item in author_div:
        author = ' '.join(item.get_text().split())

    abstract = str(abstract_div[0].contents[2])

    # ifreferen = soup.find_all('td', class_='b14', rowspan='2')
    # ref = ''
    # for i in range(len(ifreferen)):
    #     if ('【共引文献】' in ifreferen[i].get_text()):
    #         referenceList = soup.find_all('div', id='div_Ref')  # 共引文献列表
    #         if len(referenceList) == 0:
    #             referenceList = soup.find_all('div', class_='div_Ref')
    #         referenceList = referenceList[i]
    #         for tdref in referenceList.find_all('td', width='676'):
    #             refitem = tdref.a.get("href")
    #             refitem = refitem.strip()
    #             print(refitem)
    #             ref = ref + refitem + ' ,'
    # 获取作者单位，处理字符串匹配
    author_unit_scope = soup.find('div', style='text-align:left;', class_='xx_font')
    author_unit_scope_text = author_unit_scope.get_text()
    unit = ''
    if '作者单位' in author_unit_scope_text or '学位授予单位' in author_unit_scope_text:
        if category == '硕士论文' or category == '博士论文':
            unit = str(author_unit_scope.contents[2])
        elif category == '会议论文':
            unit = str(author_unit_scope.contents[2].contents[0])
        else:
            unit = str(author_unit_scope.contents[3].contents[0].replace(';', ''))
    else:
        unit = ''
    author_unit = ''
    author_unit_text = author_unit_scope.get_text()
    # print(author_unit_text)
    if '【作者单位】：' in author_unit_text:
        auindex = author_unit_text.find('【作者单位】：', 0)
    else:
        auindex = author_unit_text.find('【学位授予单位】：', 0)
    for k in range(auindex, len(author_unit_text)):
        if author_unit_text[k] == '\n' or author_unit_text[k] == '\t' or author_unit_text[k] == '\r' or \
                author_unit_text[k] == '】':
            continue
        if author_unit_text[k] == ' ' and author_unit_text[k + 1] == ' ':
            continue
        if author_unit_text[k] != '【':
            author_unit = author_unit + author_unit_text[k]
        if author_unit_text[k] == '【' and k != auindex:
            break
    # 获取关键字
    # key_word = ''
    # kwindex = author_unit_text.find('【关键词】：', 0)
    # if kwindex != -1:
    #     for k in range(kwindex, len(author_unit_text)):
    #         if author_unit_text[k] == '\n' or author_unit_text[k] == '\t' or author_unit_text[k] == '\r' or \
    #                 author_unit_text[k] == '】':
    #             continue
    #         if author_unit_text[k] == ' ' and author_unit_text[k + 1] == ' ':
    #             continue
    #         if author_unit_text[k] != '【':
    #             key_word = key_word + author_unit_text[k]
    #         if author_unit_text[k] == '【' and k != kwindex:
    #             break
    return temp_paper
