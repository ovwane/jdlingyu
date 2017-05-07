#!/bin/env python3
# -*- coding: utf-8 -*-

'''
爬虫 for 单个主题页面 如:http://www.jdlingyu.moe/16289/ --- 你懂的！
'''

__author__ = 'Otokaze 738158186@qq.com'

def jdlingyu():
    import requests,logging,os,re,html

    logger=logging.getLogger(os.path.abspath(__file__))
    logger.setLevel(logging.ERROR)
    handler=logging.FileHandler('jdlingyu_theme.log')
    handler.setLevel(logging.ERROR)
    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    current_os=os.name
    if current_os == 'posix':
        path_format=r'/root/jdlingyu'
    elif current_os == 'nt':
        path_format=r'd:/jdlingyu'

    while True:
        url=input('url(eg: http://www.jdlingyu.moe/16289/): ').strip().lower()
        re_chk_url=re.compile(r'^http(?:s)?://[^\s]+$')
        chk_url=re.search(re_chk_url,url)
        if chk_url != None:
            break

    while True:
        path=input('save_path(eg: %s): ' % path_format).strip()
        if current_os == 'posix':
            re_chk_path=re.compile(r'^/[^/\s].*$')
            chk_path=re.search(re_chk_path,path)
            if chk_path != None:
                if not os.path.isdir(path):
                    os.mkdir(path)
                break
        elif current_os == 'nt':
            re_chk_path=re.compile(r'^[c-zC-Z]:/[^\s].*$')
            chk_path=re.search(re_chk_path,path)
            if chk_path != None:
                if not os.path.isdir(path):
                    os.mkdir(path)
                break

    headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
    'Connection':'close'
    }
    try:
        r=requests.get(url,headers=headers)
        r.encoding='utf-8'
        data_html=r.text
        r.close()
        re_title=re.compile(r'<title>(.*?)</title>')
        re_pic1=re.compile(r'(http://www.jdlingyu.moe/wp-content/uploads/\d{4}/\d{2}/(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(?:-\d+?)?\.(?:jpg|jpeg|png|gif)))')
        re_pic2=re.compile(r'(http://ww\d.sinaimg.cn/large/(.*?\.(?:jpg|jpeg|png|gif)))')
        ex_pic={
        'http://www.jdlingyu.moe/wp-content/uploads/2016/02/2016-02-04_17-40-21.png',
        'http://www.jdlingyu.moe/wp-content/uploads/2016/09/2016-09-17_16-28-29.jpg',
        'http://www.jdlingyu.moe/wp-content/uploads/2016/10/2016-10-14_13-50-19.jpg',
        'http://www.jdlingyu.moe/wp-content/uploads/2016/11/2016-11-04_16-16-09.jpg',
        'http://www.jdlingyu.moe/wp-content/uploads/2016/03/2016-03-07_16-37-20.png',
        'http://www.jdlingyu.moe/wp-content/uploads/2016/07/2016-07-23_16-12-13.jpg',
        'http://www.jdlingyu.moe/wp-content/uploads/2016/09/2016-09-17_16-31-37.jpg',
        'http://www.jdlingyu.moe/wp-content/uploads/2016/07/2016-07-23_15-53-05.jpg',
        'http://www.jdlingyu.moe/wp-content/uploads/2016/10/2016-10-30_00-47-09.png',
        'http://www.jdlingyu.moe/wp-content/uploads/2016/10/2016-10-03_22-10-06.jpg',
        'http://www.jdlingyu.moe/wp-content/uploads/2016/10/2016-10-03_22-15-50.jpg',
        'http://www.jdlingyu.moe/wp-content/uploads/2016/08/2016-08-22_11-15-19.jpg',
        'http://www.jdlingyu.moe/wp-content/uploads/2017/01/2017-01-07_20-57-14.png',
        'http://www.jdlingyu.moe/wp-content/uploads/2017/01/2017-01-07_00-26-46.png'
        }
    
        title=html.unescape(re.search(re_title,data_html).group(1))
        path_title=os.path.join(path,title)
        if not os.path.isdir(path_title):
            os.mkdir(path_title)
        pic1=re.findall(re_pic1,data_html)
        pic2=re.findall(re_pic2,data_html)
        pic=pic1+pic2
        print('\n------------------------ %s -----------------------' % url)
        for picurl,picname in pic:
            if picurl in ex_pic:
                continue
            path_pic=os.path.join(path_title,picname)
            print('url: %s' % picurl)
            try:
                with open(path_pic,'wb') as f:
                    r_pic=requests.get(picurl,headers=headers)
                    for chunk in r_pic.iter_content(1024):
                        f.write(chunk)
                    r_pic.close()
            except BaseException as e:
                logger.error(e)
    except BaseException as e:
        logger.error(e)

if __name__ == '__main__':
    jdlingyu()
