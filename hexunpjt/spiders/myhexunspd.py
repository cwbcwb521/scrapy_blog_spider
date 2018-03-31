# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request
from hexunpjt.items import HexunpjtItem
from scrapy.http import Request

CHECK_NEXT_URL = 1

class MyhexunspdSpider(scrapy.Spider):
    name = "myhexunspd"
    allowed_domains = ["hexun.com"]
    uid = 'shihanbingblog'
    start_urls = (
        'http://fjrs168.blog.hexun.com/',
    )

    def start_requests(self):
        # 首次爬取模拟成浏览器
        yield Request("http://" + str(self.uid) + ".blog.hexun.com/p1/default.html",headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}  )

    def parse(self, response):
        item = HexunpjtItem()
        item['name'] = response.xpath('//span[@class="ArticleTitleText"]/a/text()').extract()
        item['url'] = response.xpath('//span[@class="ArticleTitleText"]/a/@href').extract()
        # 使用urllib和re模块获取博文的评论数和阅读数
        # 首先提取存储评论数和点击数网址的正则表达式
        # url click&comment
        pat1 = '<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">'
        # hcurl 为存储评论数和点击数的网址
        hcurl = re.compile(pat1).findall(str(response.body))[0]
        # 模拟成浏览器
        headers2 = ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers2]
        # 将 opener 安装为全局
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(hcurl).read()
        # pat2 为提取文章阅读数的正则
        pat2 = "click\d*?','(\d*?)'"
        # pat3 为评论数的正则
        pat3 = "comment\d*?','(\d*?)'"
        # 赋值给item
        item['hits'] = re.compile(pat2).findall(str(data))
        item['comment'] = re.compile(pat3).findall(str(data))

        yield item

        # 提取文章列表总数
        pat4 = 'blog.hexun.com/p(.*?)/'
        # 通过正则表达式获取到的数据为一个列表，倒数第二个为总页数
        data2 = re.compile(pat4).findall(str(response.body))
        if(len(data2)>=2):
            totalurl = data2[-2]
        else:
            totalurl = 1
        # print('totalurl' + str(totalurl))
        print(str(response.url))
        # 判断是否需要生成所有连接

        # for 循环，依次爬取各博文列表的博文数据
        global CHECK_NEXT_URL
        if CHECK_NEXT_URL == 1:
            for i in range(2, int(totalurl) + 1):
                CHECK_NEXT_URL = 0
                # 构造下一次要爬取的url, 爬取下一页博文列表中的数据
                nexturl = "http://" + str(self.uid) + ".blog.hexun.com/p" + str(i) + "/default.html"
                # 进行下一次爬取，模拟浏览器运行
                yield Request(nexturl, callback=self.parse, headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}  )
                # print(nexturl)
