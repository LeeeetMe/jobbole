# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']
    post_num = 0

    def parse(self, response):

        # 1、获取文章列表中文章的url，并下载
        # 2、通过文章url解析文章内容
        # 3、获取下一页的url，并交给scrapy下载
        # 1、获取文章列表中文章的url，并下载

        # 通过xpath获取
        # url_list = response.xpath('//div[@class="grid-8"]/div/div[@class="post-thumb"]/a/@href').extract()
        url_nodes = response.css('.grid-8 > div .post-thumb a')

        for url_node in url_nodes:
            post_url = url_node.css('::attr(href)').extract_first("")
            front_img_url = url_node.css('img::attr(src)').extract_first("")

            post_url = parse.urljoin(response.url,post_url)
            front_img_url = parse.urljoin(response.url,front_img_url)
            # 交给parse_detail解析
            yield Request(url=post_url,callback=self.parse_detail,meta={'front_img_url':front_img_url})
        # 获取下一页的url
        # 通过xpath获取
        # next_page = response.xpath('//*[@id="archive"]/div[21]/a[4]/@href').extract_first()
        # 通过css获取
        next_page = response.css('.next.page-numbers::attr(href)').extract_first()
        yield Request(next_page,callback=self.parse)

    def parse_detail(self,response):
        '''
            解析文章具体内容
        '''
        # 标题
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        title = response.css('.entry-header h1::text').extract_first()
        print('title==',title)

        #点赞数
        # up_count = response.xpath('//div[@class="post-adds"]/span[1]/h10/text()').extract_first()
        up_count = response.css('.post-adds>:first-child h10::text').extract_first()
        #收藏数
        # collect_count = response.xpath('//div[@class="post-adds"]/span[2]/text()').extract_first()
        collect_count = response.css('.post-adds span:nth-child(2)').extract_first()
        collect_match = re.match('.*?(\d+).*',collect_count)
        if collect_match:
            collect_count = collect_match.group(1)
        else:
            collect_count = '0'
        #评论数
        # comment_count = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first()
        comment_count = response.css('a[href="#article-comment"] span::text').extract_first()
        comment_match = re.match('.*?(\d+).*',comment_count)
        if comment_match:
            comment_count = comment_match.group(1)
        else:
            comment_count = '0'
        # 创建时间
        # create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first()
        create_date = response.css('.entry-meta-hide-on-mobile::text').extract_first()
        create_date = create_date.replace('·','').strip()
        # 文章分类
        # category = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a[1]/text()').extract_first()
        category = response.css('.entry-meta-hide-on-mobile a:nth-child(1)::text').extract_first()

        # tag分类.list
        # tag = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a[contains(@href,"/tag/")]/text()').extract()
        tag = response.css('.entry-meta-hide-on-mobile a[href*="/tag/"]::text').extract()

        # 文章详细
        # content = response.xpath('//div[@class="entry"]').extract_first()
        content = response.css('.entry').extract_first()