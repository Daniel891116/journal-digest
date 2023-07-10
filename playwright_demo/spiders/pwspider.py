import scrapy
from scrapy_playwright.page import PageMethod
from playwright_demo.items import LOAC_article
from typing import List
class PwspiderSpider(scrapy.Spider):
    name = 'pwspider'
    website = 'https://pubs.rsc.org'
    def start_requests(self):
        yield scrapy.Request(
            url='https://pubs.rsc.org/en/journals/journalissues/lc#!recentarticles&adv',
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod(
                        'wait_for_selector',
                        'div.tab-content > div:nth-child(5) > a > div.capsule__column-wrapper > div.capsule__article-image > img',
                        timeout=600
                    )
                ]   
            )
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        article = LOAC_article()
        for item in response.css('div.tab-content div.capsule--article'):
            await page.wait_for_selector('img', timeout=400)
            article['title'] = self.list_to_str_seq(item.css('h3.capsule__title::text').getall())
            article['author'] = item.css('div.article__authors::text').get().strip()
            article['content'] = item.css('p::text').get()
            article['toc_figure'] = self.website + item.css('div.capsule__article-image img').xpath('@data-original').get()
            article['doi'] = item.css('div.capsule__footer a::attr(href)').get()
            article['link'] = self.website + item.css('a.capsule__action::attr(href)').get()
            yield article

            # yield scrapy.Request(
            #     url=article['link'],
            #     meta=dict(
            #         playwright=True,
            #         playwright_include_page=True,
            #         playwright_page_methods=[
            #             PageMethod(
            #                 'wait_for_selector',
            #                 'article.article-control',
            #                 timeout=600
            #             )
            #         ]   
            #     ),
            #     callback=self.parse
            # )
            
    def list_to_str_seq(self, list: List) -> str:
        if len(list) == 1:
            return list[0].strip()
        else:
            __str = ''
            for _str in list:
                __str += _str.strip()
            return __str
        