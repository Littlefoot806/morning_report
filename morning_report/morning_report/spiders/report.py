# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import urllib


class ReportSpider(scrapy.Spider):
    name = 'report'
    allowed_domains = ['']
    # url_to_send_message = "https://api.telegram.org/bot1149905775:AAH3E0Mvhi9d1itnCBSNY85Il5TLZqhijYU/sendMessage?chat_id=342491940&text={}" # tuchka
    url_to_send_message = "https://api.telegram.org/bot1149905775:AAH3E0Mvhi9d1itnCBSNY85Il5TLZqhijYU/sendMessage?chat_id=211507050&text={}"  # I'm

    def start_requests(self):
        urls = [
            "https://nibulon.com/data/zakupivlya-silgospprodukcii/zakupivelni-cini.html",
            "https://obmenka.kharkov.ua/usd-uah",
            "https://obmenka.kharkov.ua/eur-uah",
            "https://prometey.org.ua/zakupochny-e-tseny-na-e-levatorah/?_sft_culture=yachmin",
        ]

        for url in urls:
            if "nibulon" in url:
                body = {"culture": "101000000000001", "bazis": "47834",
                        "priceDate": "5a0ea51b6667f940de3c4072202976b6"}
                yield FormRequest(url, formdata=body, callback=self.parse_nibulon)
            elif "prometey" in url:
                yield Request(url, callback=self.parse_prometey)
            elif "usd-uah" in url:
                yield Request(url, callback=self.parse_usd)
            elif "eur-uah" in url:
                yield Request(url, callback=self.parse_eur)

    def parse_nibulon(self, response):

        price = response.xpath(
            '//div[@class="culture_head collapsed"]/descendant::text()').extract()
        clean_price = ''.join([i.strip() for i in price if i])
        result = "Nibulon:\n"+clean_price
        # result = clean_price.encode("UTF-8")

        yield Request(self.url_to_send_message.format(result), dont_filter=True, callback=self.ok)

    def parse_usd(self, response):

        # uah-usd
        buy = response.xpath(
            """//li[@class="pair__block"][1]//div[contains(@class, 'block-retail')]/div[contains(@class, 'block-num')]/text()"""
        ).extract_first()

        sell = response.xpath(
            """//li[@class="pair__block"][2]//div[contains(@class, 'block-retail')]/div[contains(@class, 'block-num')]/text()"""
        ).extract_first()

        result = "UAH-USD\nПокупка: {buy}\nПродажа: {sell}".format(
            buy=buy, sell=sell)
        result = urllib.quote(result)
        yield Request(self.url_to_send_message.format(result), dont_filter=True, callback=self.ok)

    def parse_eur(self, response):

        # uah-eur
        buy = response.xpath(
            """//li[@class="pair__block"][1]//div[contains(@class, 'block-retail')]/div[contains(@class, 'block-num')]/text()"""
        ).extract_first()

        sell = response.xpath(
            """//li[@class="pair__block"][2]//div[contains(@class, 'block-retail')]/div[contains(@class, 'block-num')]/text()"""
        ).extract_first()

        result = "UAH-EUR\nПокупка: {buy}\nПродажа: {sell}".format(
            buy=buy, sell=sell)
        result = urllib.quote(result)
        yield Request(self.url_to_send_message.format(result), dont_filter=True, callback=self.ok)

    def parse_prometey(self, response):

        price = "".join(response.xpath(
            """//div[@class="priceblock"][1]//div[contains(@class, "coin")][last()]//div[contains(@class,"coin_title")]/text()"""
        ).extract())
        result = "Prometey:\n" + price.split(",")[0].strip()

        yield Request(self.url_to_send_message.format(result), dont_filter=True, callback=self.ok)

    def ok(self, response):
        yield {"ok": "ok"}
