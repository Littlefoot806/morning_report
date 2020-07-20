# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import urllib


class ReportSpider(scrapy.Spider):
    name = 'report'
    allowed_domains = ['']
    url_to_send_message = "https://api.telegram.org/bot1149905775:AAH3E0Mvhi9d1itnCBSNY85Il5TLZqhijYU/sendMessage?chat_id=211507050&text={}"

    def start_requests(self):
        urls = ["https://nibulon.com/data/zakupivlya-silgospprodukcii/zakupivelni-cini.html",
                "https://obmenka.kharkov.ua/usd-uah"]
        body = {"culture": "101000000000001", "bazis": "47834", "priceDate": "5a0ea51b6667f940de3c4072202976b6"}

        for url in urls:
            if "nibulon" in url:
                yield FormRequest(url, formdata=body, callback=self.parse_price)
            else:
                yield Request(url, callback=self.parse_usd)

    def parse_price(self, response):

        price = response.xpath('//div[@class="culture_head collapsed"]/descendant::text()').extract()
        clean_price = ''.join([i.strip() for i in price if i])
        clean_price = urllib.quote(clean_price)
        yield Request(self.url_to_send_message.format(clean_price), dont_filter=True, callback=self.ok)

    def parse_usd(self, response):

        # uah-usd
        buy = response.xpath(
            """//li[@class="pair__block"][1]//div[contains(@class, 'block-retail')]/div[contains(@class, 'block-num')]/text()"""
        ).extract_first()
        move_buy = response.xpath(
            """//li[@class="pair__block"][1]//div[contains(@class, 'block-retail')]/div[contains(@class, 'block-move')]/span/text()"""
        ).extract_first()

        sell = response.xpath(
            """//li[@class="pair__block"][2]//div[contains(@class, 'block-retail')]/div[contains(@class, 'block-num')]/text()"""
        ).extract_first()
        move_sell = response.xpath(
            """//li[@class="pair__block"][2]//div[contains(@class, 'block-retail')]/div[contains(@class, 'block-move')]/span/text()"""
        ).extract_first()

        try:
            move_buy = int(move_buy)
        except:
            move_buy = 0

        try:
            move_sell = int(move_sell)
        except:
            move_sell = 0

        result = "$$$%0AПокупка: {buy}%0AИзменение за день: {move_buy}%0AПродажа: {sell}%0AИзменение за день: {move_sell}".format(buy=buy, move_buy=move_buy, sell=sell, move_sell=move_sell)
        result = urllib.quote(result)
        yield Request(self.url_to_send_message.format(result), dont_filter=True, callback=self.ok)

    def ok(self, response):
        yield {"ok": "ok"}
