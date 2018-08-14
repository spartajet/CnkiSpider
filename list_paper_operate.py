__author__ = 'Xiaozhong GUO'
import urllib
from bs4 import BeautifulSoup
import paper
import logging

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


def operate_list_paper(list_paper_url, category):
    html = urllib.request.urlopen(list_paper_url).read()
    soup = BeautifulSoup(html, 'html.parser')

    all_divs = soup.find_all('div', class_='wz_content')
    papers = []
    for string in all_divs:
        item = string.find('a', target='_blank')  # 文章标题与链接
        href = item.get('href')  # 获取文章url
        if 'www.cnki.com.cn' not in href:
            continue
        logger.info('current paper info link {}'.format(href))
        title = item.get_text()  # 获取文章标题
        year_count = string.find('span', class_='year-count')  # 获取文章出处与引用次数
        # year_count = year_count.get_text()
        publisher = ''
        # reference = ''
        year = 1900
        publish_year_string = year_count.contents[0].string.replace('\xa0\xa0', ' ')
        publish_year_string_items = publish_year_string.split(' ')
        if category == '学术期刊':
            publisher = publish_year_string_items[0].lstrip('《').rstrip('》')
            year = int(publish_year_string_items[1].replace('年', ''))
        elif category == '博士论文' or category == '硕士论文':
            publisher = publish_year_string_items[0]
            year = int(publish_year_string_items[2].replace('年', ''))
        elif category == '会议论文':
            publisher = publish_year_string_items[0].lstrip('《').rstrip('》')
            year = int(publish_year_string_items[1][:4])

        download_cite_items = year_count.contents[2].string.split('|')
        download_end_index = download_cite_items[0].index('）')
        if download_end_index == 5:
            download = 0
        else:
            download = int(download_cite_items[0][5:download_end_index])
        cite_end_index = download_cite_items[1].index('）')
        if cite_end_index == 6:
            cite = 0
        else:
            cite = int(download_cite_items[1][6:cite_end_index])
            try:
                temp_paper = paper.create_paper(href, category, title, publisher, year, download, cite)
                papers.append(temp_paper)
            except:
                logger.info('paper spider fail url {}'.format(href))
    return papers


def insert_papers_into_database(papers):
    pass
