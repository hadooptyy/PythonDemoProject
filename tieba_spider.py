# coding=utf-8

import urllib.request


def write_to_file(file_name, html):
    '''
    将抓取的html写入到文件中
    '''
    print('正在写入文件', file_name)
    f = open(file_name, 'w', encoding='UTF-8')
    f.write(str(html))
    f.close()


def tieba_spider(url):
    '''
    百度贴吧小爬虫
    '''
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    headers = {'User-Agent': user_agent}
    opener = urllib.request.build_opener()
    html = opener.open(url).read()
    html = html.decode('UTF-8')
    return html

# 主程序
if __name__ == "__main__":
    name = input('请输入要爬取的链接：')
    beginpage = int(input('请输入要爬取的起始页数：'))
    endpage = int(input('请输入要爬取的终止页数：'))
    for i in range(beginpage, endpage + 1):
        url = name + str((i - 1) * 50)
        html = tieba_spider(url)
        file_name = str(i) + '.html'
        write_to_file(file_name, html)
