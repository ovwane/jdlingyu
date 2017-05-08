#!/bin/env python3
# -*- coding: utf-8 -*-

'''
爬虫 for 单个主题页面 如:http://www.jdlingyu.moe/16289/ --- 你懂的！
'''

__author__ = 'Otokaze 738158186@qq.com'

def jdlingyu():
    import requests,logging,os,re,html,argparse,sys

    # logger
    logger=logging.getLogger(os.path.abspath(__file__))
    logger.setLevel(logging.ERROR)
    handler=logging.FileHandler('{}.log'.format(os.path.splitext(__file__)[0]))
    handler.setLevel(logging.ERROR)
    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # argparse
    parser=argparse.ArgumentParser(description='parse pictures from http://www.jdlingyu.moe')
    parser.add_argument('url', help='To download the URL path')
    parser.add_argument('-o', '--output_path', help='Specify file save path', default=os.path.join(os.path.abspath('.'), 'download'))
    parser.add_argument('-q', '--quiet', help='Do not display output information', action='store_true')
    args=parser.parse_args()

    # 参数检查 - url
    if type(args.url) != type(None):
        url_pre=args.url.strip().lower()
        re_chk_url=re.compile(r'^http(?:s)?://[^\s]+$')
        chk_url=re.search(re_chk_url,url_pre)
        if chk_url != None:
            url=url_pre
        else:
            print('Input is not standard URL!')
            sys.exit(1)
    else:
        print('You don\'t enter anything!')
        sys.exit(1)

    # 参数检查 - path
    path_pre=args.output_path.strip()
    current_os=os.name
    if current_os == 'posix':
        re_chk_path=re.compile(r'^\/.*')
        re_chk_path_current=re.compile(r'^[^\/].*')
        chk_path=re.search(re_chk_path,path_pre)
        chk_path_current=re.search(re_chk_path_current,path_pre)
        if chk_path != None:
            path=path_pre
            if not os.path.isdir(path):
                os.mkdir(path)
        elif chk_path_current !=  None:
            path=os.path.join(os.path.abspath('.'), path_pre)
            if not os.path.isdir(path):
                os.mkdir(path)
    elif current_os == 'nt':
        re_chk_path=re.compile(r'^[a-zA-Z]:.*')
        re_chk_path_current=re.compile(r'^[^a-zA-Z][^:].*')
        chk_path=re.search(re_chk_path,path_pre)
        chk_path_current=re.search(re_chk_path_current,path_pre)
        if chk_path != None:
            path=path_pre
            if not os.path.isdir(path):
                os.mkdir(path)
        elif chk_path_current != None:
            path=os.path.join(os.path.abspath('.'), path_pre)
            if not os.path.isdir(path):
                os.mkdir(path)

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
            except Exception as e:
                logger.error(e)
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    jdlingyu()
