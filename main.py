import os
import time
import urllib

from requests import Response

import util
from douyin import Douyin
from util import logger


def generate_archive_md(searches):
    """生成今日readme
    """
    def search(item):
        word = item['word']
        url = 'https://www.douyin.com/search/' + urllib.parse.quote(word)
        return '1. [{}]({})'.format(word, url)



    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])


    readme = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        readme = f.read()

    now = util.current_time()
    readme = readme.replace("{updateTime}", now)
    readme = readme.replace("{searches}", searchMd)

    return readme


def generate_readme(searches):
    """生成今日readme
    """
    def search(item):
        word = item['word']
        url = 'https://www.douyin.com/search/' + urllib.parse.quote(word)
        return '1. [{}]({})'.format(word, url)

    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    readme = ''
    file = os.path.join('template', 'README.md')
    with open(file) as f:
        readme = f.read()

    now = util.current_time()
    readme = readme+searchMd

    return readme

def redmd()
    now = util.current_time()
    files = os.path.join('raw', now)
    g = os.walk(files)
    readme = ''
    readmes = ''
    for path,dir_list,file_list in g:  
          for file_name in file_list: 
              file=(os.path.join(path, file_name) 
               with open(file) as f:
                   readme = f.read()
               readmes=readmes+readme
               filee = os.path.join('archives', 'guagua.md')
               util.write_text(filee, readmes)

def save_readme(md):
    
     now = util.current_time()
     filename = now +'.md'
     date = util.current_date()
     file = os.path.join('raw', date, filename)
     util.write_text(file, md)


def save_archive_md(md):
    logger.info('archive md:%s', md)
    name = util.current_date()+'.md'
    file = os.path.join('archives', name)
    util.write_text(file, md)

def save_raw_response(resp: Response, filename: str):
    """保存原始响应内容
    """
    if resp:
        content = resp.text
        
        filename = '{}.json'.format(filename)
        logger.info('save response:%s', filename)
        date = util.current_date()
        file = os.path.join('raw', date, filename)
        util.write_text(file, content)


def run():
    # 获取数据
    dy = Douyin()
    # 热搜
    now = util.current_time()
    searches, resp = dy.get_hot_search()
    save_raw_response(resp, 'hot-search')
    time.sleep(1)


    # 最新数据
    todayMd = generate_readme(searches)
    save_readme(todayMd)
    redmd()
    # 归档
    archiveMd = generate_archive_md(searches)
    save_archive_md(archiveMd)


if __name__ == "__main__":
    try:
        run()
    except:
        logger.exception('run failed')
