# coding=utf-8

'''
    Python小爬虫，Python3.5
    @author Wells
    @version v1.0
    @date 2016-04-04
'''

import urllib.request
import re
import time
import os
import random


class SpiderTest:
    '''
    爬虫类
    '''

    def __init__(self):
        # 开始页数
        self.page = 1
        # 状态标记
        self.enable = True

    def load_page_html(self, url, code):
        '''
        根据url请求目标服务器获取网页内容
        '''
        # 伪装成浏览器并请求服务器
        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        headers = ('User-Agent', user_agent)
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        html = opener.open(url).read().decode(code, 'ignore')
        return html

    def get_data(self, page):
        '''
        根据正则表达式过滤数据
        '''
        url = 'http://voice.hupu.com/nba/' + str(page)
        print('正在爬取第%d页数据...' % (self.page))
        html = self.load_page_html(url, 'utf-8')
        pattern = re.compile(
            r'<h4>.*?<a.*?href="http://voice.hupu.com/nba/(\d+)\.html".*?target="_blank".*?>(.*?)</a>.*?</h4>', re.S)
        items = pattern.findall(html)
        print('第%d页数据爬取完毕，第%d页共爬取到%d条数据！准备根据链接爬取相应的正文内容' %
              (page, page, len(items)))
        print('\n')
        # 判断是否抓取到数据标题及链接地址
        if len(items) != 0:
            for index in range(0, len(items)):
                child_url = 'http://voice.hupu.com/nba/' + \
                    str(items[index][0]) + '.html'
                # 随机产生一个整数，等待多少秒再进行下一次请求
                time.sleep(random.randint(3, 7))
                print('正在爬取第%d页第%d条数据内容...' % (page, index + 1))
                print(' ★ ' + items[index][1] + ' ★ ' + child_url)
                child_html = self.load_page_html(child_url, 'utf-8')
                child_pattern = re.compile(
                    r'<div.*?class="artical-main-content".*?>(.*?)</div>', re.S)
                child_item = child_pattern.findall(child_html)
                print('第%d页第%d条数据内容爬取完毕！准备写入到文件中' % (page, index + 1))
                # 判断是否抓取到对应项数据的网页正文内容
                if len(child_item) != 0:
                    new_item = child_item[0].replace(
                        '<p>', '').replace('<span id="editor_baidu">', '').replace('</span>', '').replace('</p>', '').replace('&nbsp;', '').replace('&rdquo;', '').replace('&ldquo;', '').replace('&hellip;', '').replace('&lsquo;', '').replace('&rsquo;', '').replace('<br />', '').replace('<span style="line-height: 1.6em;">', '').replace('&mdash;', '').replace('<strong>', '').replace('</strong>', '')
                    file_name = items[index][1].replace('?', '') + '.txt'
                    self.write_to_file(page, index + 1, 'd:\\Download\\TestData\\',
                                       file_name, 'UTF-8', new_item)
                    # 判断该条数据是否是当前页的最后一条
                    if (index + 1) == len(items):
                        print('第%d页数据已全部写完！' % (page))
                        print(
                            '========================================================')
                else:
                    print('非常抱歉，第%d页%d条数据内容获取不到！' % (page, index + 1))
                    print('\n')

    def write_to_file(self, page, index, dir_name, file_name, code, text):
        '''
        把数据写入文件中，参数依次表示当前页码，该条数据的索引，目录名，文件名，编码，数据内容
        '''
        # 拼接目录绝对路径
        dir_path = dir_name + "page_" + str(page)
        # 判断目录是否存在，不存在就创建该目录
        if os.path.exists(dir_path) == False:
            os.makedirs(dir_path)
            print('page_' + str(page), '目录创建成功，开始写入第%d页数据！' % (page))
        # 拼接文件全路径名
        file_path = dir_path + '\\' + file_name
        # 判断文件是否存在，存在的话就结束操作，操作下一条数据
        if os.path.exists(file_path):
            print('第%d页第%d条数据已存在，跳过该条数据...' % (page, index))
            print('\n')
            return
        # 开始写数据
        print('正在写入第%d页第%d条数据...' % (page, index))
        f = open(file_path, 'w', encoding=code)
        f.write(str(text))
        f.close()
        print('第%d页第%d条数据写入完毕！' % (page, index))
        print('\n')

    def dowork(self):
        '''
        开启爬虫
        '''
        print('★★★爬虫程序已启动，请按提示信息操作★★★')
        while self.enable:
            print('---按回车键继续爬取，输入quit退出---')
            myinput = input()
            if myinput != 'quit':
                print('准备爬取第%d页数据，获取标题及对应链接地址' % (self.page))
                self.get_data(self.page)
                self.page += 1
            else:
                self.enable = False
                break

# 主程序
if __name__ == "__main__":
    # 创建爬虫对象
    spider = SpiderTest()
    # 爬虫开始工作
    spider.dowork()
