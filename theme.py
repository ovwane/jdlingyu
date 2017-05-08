#!/bin/env python3
# -*- coding: utf-8 -*-

'''
爬虫 for 单个主题页面 如:http://www.jdlingyu.moe/16289/ --- 你懂的！
'''

__author__ = 'Otokaze 738158186@qq.com'

def jdlingyu():
    import requests,logging,os,re,html,argparse,sys

    # argparse
    parser=argparse.ArgumentParser(description='parse pictures from http://www.jdlingyu.moe')
    parser.add_argument('url', help='To download the URL path')
    parser.add_argument('-o', '--output_path', help='Specify file save path', default=os.path.join(os.path.abspath('.'), 'download'))
    parser.add_argument('-l', '--log', help='save log to file', action='store_true')
    parser.add_argument('-q', '--quiet', help='Do not display output information', action='store_true')
    parser.add_argument('-v', '--version', help='Display program version', action='version', version='jdlingyu.py v2.0')
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

    # 参数检查 - log
    if args.log:
        logger=logging.getLogger(os.path.abspath(__file__))
        logger.setLevel(logging.ERROR)
        handler=logging.FileHandler('{}.log'.format(os.path.splitext(__file__)[0]))
        handler.setLevel(logging.ERROR)
        formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
    'Connection':'close'
    }

    try:
        # 排除无关图片
        ## 样本1
        r_exclude_1=requests.get('http://www.jdlingyu.moe/28721/', headers=headers)
        r_exclude_1.encoding='utf-8'
        data_html_exclude_1=r_exclude_1.text
        r_exclude_1.close()
        re_exclude_1_all_pic1=re.compile(r'http://www.jdlingyu.moe/wp-content/uploads/\d{4}/\d{2}/\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(?:-\d+?)?\.(?:jpg|jpeg|png|gif)')
        re_exclude_1_all_pic2=re.compile(r'http://ww\d.sinaimg.cn/large/(.*?\.(?:jpg|jpeg|png|gif))')
        re_exclude_1_all_pic=re.findall(re_exclude_1_all_pic1, data_html_exclude_1) + re.findall(re_exclude_1_all_pic2, data_html_exclude_1)
        ## 样本2
        r_exclude_2=requests.get('http://www.jdlingyu.moe/16289/', headers=headers)
        r_exclude_2.encoding='utf-8'
        data_html_exclude_2=r_exclude_2.text
        r_exclude_2.close()
        re_exclude_2_all_pic1=re.compile(r'http://www.jdlingyu.moe/wp-content/uploads/\d{4}/\d{2}/\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(?:-\d+?)?\.(?:jpg|jpeg|png|gif)')
        re_exclude_2_all_pic2=re.compile(r'http://ww\d.sinaimg.cn/large/(.*?\.(?:jpg|jpeg|png|gif))')
        re_exclude_2_all_pic=re.findall(re_exclude_2_all_pic1, data_html_exclude_2) + re.findall(re_exclude_2_all_pic2, data_html_exclude_2)
        ## 获取无关图片url
        exclude_1=set(re_exclude_1_all_pic)
        exclude_2=set(re_exclude_2_all_pic)
        ex_pic=exclude_1 & exclude_2

        # requests_get
        r=requests.get(url,headers=headers)
        r.encoding='utf-8'
        data_html=r.text
        r.close()

        # regexp预编译
        re_title=re.compile(r'<title>(.*?)</title>')
        re_pic1=re.compile(r'(http://www.jdlingyu.moe/wp-content/uploads/\d{4}/\d{2}/(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(?:-\d+?)?\.(?:jpg|jpeg|png|gif)))')
        re_pic2=re.compile(r'(http://ww\d.sinaimg.cn/large/(.*?\.(?:jpg|jpeg|png|gif)))')

        # 获取title
        title=html.unescape(re.search(re_title,data_html).group(1))
        path_title=os.path.join(path,title)
        if not os.path.isdir(path_title):
            os.mkdir(path_title)

        # 获取picture_urls
        pic1=re.findall(re_pic1,data_html)
        pic2=re.findall(re_pic2,data_html)
        pic=set(pic1) | set(pic2)

        # 保存图片
        # 参数检查 - quiet
        if not args.quiet:
            print('\n------------------------ %s -----------------------' % url)
        for picurl,picname in pic:
            if picurl in ex_pic:
                continue
            path_pic=os.path.join(path_title,picname)
            # 参数检查 - quiet
            if not args.quiet:
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
