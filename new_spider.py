# coding=utf-8

'''
    Python小爬虫，Python3.5
    @author Wells
    @version v1.0
    @date 2016-04-01
'''

import urllib.request
import re


class Spider:
    '''
    爬虫类
    '''

    def __init__(self):
        # 开始页数
        self.start_page = 1
        # 状态标记
        self.enable = True

    def load_page(self, page):
        '''
        根据url请求目标服务器获取网页内容
        '''
        url = 'http://www.neihan8.com/article/list_5_' + str(page) + '.html'
        # 伪装成浏览器并请求服务器
        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        headers = ('User-Agent', user_agent)
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        html = opener.open(url).read().decode('GBK',)
        # 正则匹配
        pattern = re.compile(r'<div.*?class="f18 mb20">(.*?)</div>', re.S)
        items = pattern.findall(html)
        # 过滤提取匹配后的数据，存储到磁盘
        for item in items:
            item = item.replace('<p>', '').replace(
                '</p>', '').replace('<br />', '').replace('&ldquo;', '').replace('&rdquo;', '').replace('&hellip;', '').replace('&nbsp;', '').replace('&lsquo;', '').replace('&rsquo;', '')
            self.write_to_file(item)

    def write_to_file(self, text):
        '''
        将爬取过滤后的信息存储到磁盘文件中
        '''
        f = open('full.txt', 'a', encoding='GBK')
        f.write(str(text))
        f.close()

    def dowork(self):
        print('爬虫程序已启动，请按提示信息操作')
        while self.enable:
            print('按回车键继续爬取，输入quit退出')
            myinput = input()
            if myinput != 'quit':
                print('正在爬取第%d页...' % (self.start_page))
                self.load_page(self.start_page)
                print('正在存储第%d页数据到本地...' % (self.start_page))
                self.write_to_file(
                    '===================================================================================================================')
                self.start_page += 1
            else:
                self.enable = False
                break

# 主程序
if __name__ == "__main__":
    spider = Spider()
    # 启动爬虫
    spider.dowork()
