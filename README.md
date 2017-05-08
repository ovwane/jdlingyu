# jdlingyu.moe 图片爬虫 - python3.x
## 更新 20170508
- 基于python3.x的一个小爬虫
- 支持linux、windows - python3.x
- 需要安装requests第三方模块 `pip install requests`
- site.py支持多线程，默认5个线程，-j参数可指定线程数
- 线程数不宜过多，会导致http连接数过多，服务器拒绝连接，还可能被拉小黑屋
- 引入argparse模块

## 用法
- `git clone https://github.com/zfl9/jdlingyu.git`
- `cd jdlingyu`
- `python3 theme.py THEME_URL` - 获取单个theme的图片
- `python3 site.py` - 获取整个site的图片(多线程)
- `-o output_path` - 指定输出目录
- `-j threads_num` - 指定线程数
- `-l` - 记录log
- `-q` - 不输出信息
- `-h` - 获取帮助

## 更多请戳: [Otokaze's Blog](https://www.zfl9.com)
