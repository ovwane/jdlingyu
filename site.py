#!/bin/env python3
# -*- coding: utf-8 -*-

'''
爬虫 for 整个站点(http://www.jdlingyu.moe) --- 你懂的！
默认启动5个主线程，有需要的请指定参数 -j
请勿启动过多主线程,个人推荐3-8个!
请勿多次用同一IP爬取该网站，因为可能会被加入临时黑名单！
如果不幸被临时拉黑，请重启你的路由器或者其他网关，重新获取一个公网IP！
'''

__author__ = 'Otokaze j1002238565@gmail.com'

def jdlingyu():
    import requests,html,re,os,threading,sys,logging,argparse

    # argparse
    parser=argparse.ArgumentParser(description='parse pictures from http://www.jdlingyu.moe')
    parser.add_argument('-o', '--output_path', help='Specify file save path', default=os.path.join(os.path.abspath('.'), 'download'))
    parser.add_argument('-j', '--job', help='set threads num, default 5 threads', type=int, default=5)
    parser.add_argument('-l', '--log', help='save log to file', action='store_true')
    parser.add_argument('-q', '--quiet', help='Do not display output information', action='store_true')
    parser.add_argument('-v', '--version', help='Display program version', action='version', version='jdlingyu.py v2.0')
    args=parser.parse_args()

    # 参数 - path
    main_path_pre=args.output_path.strip()
    current_os=os.name
    if current_os == 'posix':
        re_chk_path=re.compile(r'^\/.*')
        re_chk_path_current=re.compile(r'^[^\/].*')
        chk_path=re.search(re_chk_path,main_path_pre)
        chk_path_current=re.search(re_chk_path_current,main_path_pre)
        if chk_path != None:
            main_path=main_path_pre
            if not os.path.isdir(main_path):
                os.mkdir(main_path)
        elif chk_path_current != None:
            main_path=os.path.join(os.path.abspath('.'), main_path_pre)
            if not os.path.isdir(main_path):
                os.mkdir(main_path)
        else:
            print('Input is not standard Path!')
            sys.exit(1)
    elif current_os == 'nt':
        re_chk_path=re.compile(r'^[a-zA-Z]:.*')
        re_chk_path_current=re.compile(r'^[^a-zA-Z][^:].*')
        chk_path=re.search(re_chk_path,main_path_pre)
        chk_path_current=re.search(re_chk_path_current,main_path_pre)
        if chk_path != None:
            main_path=main_path_pre
            if not os.path.isdir(main_path):
                os.mkdir(main_path)
        if chk_path_current != None:
            main_path=main_path_pre
            if not os.path.isdir(main_path):
                os.mkdir(main_path)
        else:
            print('Input is not standard Path!')
            sys.exit(1)

    # 参数 - job
    threads_num=args.job

    # 参数 - log
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

    def capture_page(page_url):
        r_page=requests.get(page_url,headers=headers)
        r_page.encoding='utf-8'
        data_page=r_page.text
        r_page.close()
        re_themes=re.compile(r'http://www.jdlingyu.moe/\d+/')
        themes=re.findall(re_themes,data_page)
        if page_url == index_url:
            page_num=1
        else:
            re_page_num=re.compile(r'http://www.jdlingyu.moe/page/(\d+)/')
            page_num=re.search(re_page_num,page_url).group(1)
        page_path=os.path.join(main_path,'page%s' % page_num)
        if not os.path.isdir(page_path):
            os.mkdir(page_path)
        
        def capture(url):
            try:
                r=requests.get(url,headers=headers)
                r.encoding='utf-8'
                data=r.text
                r.close()
                re_title=re.compile(r'<title>(.*?)</title>')
                title=html.unescape(re.search(re_title,data).group(1))
                title_path=os.path.join(page_path,title)
                if not os.path.isdir(title_path):   
                    os.mkdir(title_path)
                re_pic1=re.compile(r'(http://www.jdlingyu.moe/wp-content/uploads/\d{4}/\d{2}/(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(?:-\d+?)?\.(?:jpg|jpeg|png|gif)))')
                re_pic2=re.compile(r'(http://ww\d.sinaimg.cn/large/(.*?\.(?:jpg|jpeg|png|gif)))')
                pic1=re.findall(re_pic1,data)
                pic2=re.findall(re_pic2,data)
                pic=set(pic1) | set(pic2)
                for picurl,picname in pic:
                    if picurl in ex_pic:
                        continue
                    pic_path=os.path.join(title_path,picname)
                    with open(pic_path,'wb') as f:
                        try:
                            r_pic=requests.get(picurl,headers=headers)
                            for chunk in r_pic.iter_content(10240):
                                f.write(chunk)
                            r_pic.close()
                        except Exception as e:
                            logger.error(e)
            except Exception as e:
                logger.error(e)
        threads=[]
        for theme in themes:
            t=threading.Thread(target=capture,args=(theme,))
            threads.append(t)
        for thr in threads:
            thr.start()
        for thr in threads:
            if thr.isAlive():
                thr.join()
    
    index_url='http://www.jdlingyu.moe'
    r_index=requests.get(index_url,headers=headers)
    r_index.encoding='utf-8'
    data_index=r_index.text
    r_index.close()
    re_page_num=re.compile(r'http://www.jdlingyu.moe/page/(\d+)/')
    page_num_max=max(list(map(lambda x:int(x),re.findall(re_page_num,data_index))))
    other_url=['http://www.jdlingyu.moe/page/%s/' % x for x in range(2,page_num_max+1)]
    other_url.insert(0,index_url)
    pages_url=other_url
    
    m=0
    for i in range(0,len(pages_url),threads_num):
        pages_url_part=pages_url[i:i+threads_num]
        # 参数 - quiet
        if not args.quiet:
            m+=len(pages_url_part)
            per=m/len(pages_url)*100
            sys.stdout.write('当前页面段:%s-%s页    线程数:%s    总进度:%.2f%%\r' % (i,i+len(pages_url_part),threads_num,per))
        threads_page=[]
        for page_url in pages_url_part:
            t=threading.Thread(target=capture_page,args=(page_url,))
            threads_page.append(t)
        for thr in threads_page:
            thr.start()
        for thr in threads_page:
            if thr.isAlive():
                thr.join()

if __name__ == '__main__':
    jdlingyu()
