# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import urllib


class ReportSpider(scrapy.Spider):
    name = 'report'
    allowed_domains = ['']
    url_to_send_message = "https://api.telegram.org/bot1149905775:AAH3E0Mvhi9d1itnCBSNY85Il5TLZqhijYU/sendMessage?chat_id=-324457269&text={}"  # tuchka
    # url_to_send_message = "https://api.telegram.org/bot1149905775:AAH3E0Mvhi9d1itnCBSNY85Il5TLZqhijYU/sendMessage?chat_id=211507050&text={}"  # I'm

    def start_requests(self):
        urls = [
            "https://nibulon.com/data/zakupivlya-silgospprodukcii/zakupivelni-cini.html",
            "https://minfin.com.ua/currency/mb/",
            "https://prometey.org.ua/zakupochny-e-tseny-na-e-levatorah/?_sft_culture=yachmin",
        ]

        for url in urls:
            if "nibulon" in url:
                body = {"culture": "101000000000001", "bazis": "47834",
                        "priceDate": "5a0ea51b6667f940de3c4072202976b6"}
                yield FormRequest(url, formdata=body, callback=self.parse_nibulon)
            elif "prometey" in url:
                yield Request(url, callback=self.parse_prometey)
            elif "minfin" in url:
                yield Request(url, callback=self.parse_minfin)

    def parse_nibulon(self, response):

        price = response.xpath(
            '//div[@class="culture_head collapsed"]/descendant::text()').extract()

        clean_price = ''.join([i.strip() for i in price if i])
        clean_price = "Nibulon:\n"+clean_price
        result = clean_price.encode("UTF-8")

        yield Request(self.url_to_send_message.format(result), dont_filter=True, callback=self.ok)

    def parse_prometey(self, response):

        price = "".join(response.xpath(
            """//div[@class="priceblock"][1]//div[contains(@class, "coin")][last()]//div[contains(@class,"coin_title")]/text()"""
        ).extract())

        clean_price = "Prometey:\nЯчмінь - " + \
            price.split(",")[0].strip().encode("UTF-8")
        result = clean_price

        yield Request(self.url_to_send_message.format(result), dont_filter=True, callback=self.ok)

    def parse_minfin(self, response):

        # uah-usd
        buy = response.xpath(
            """//table[@class="mb-table-currency"]/tbody/tr[1]/td[2]/text()"""
        ).extract_first()

        sell = response.xpath(
            """//table[@class="mb-table-currency"]/tbody/tr[2]/td[2]/text()"""
        ).extract_first()

        result = "UAH-USD\nПокупка: {buy}\nПродажа: {sell}".format(
            buy=buy, sell=sell)
        result = urllib.quote(result)
        yield Request(self.url_to_send_message.format(result), dont_filter=True, callback=self.ok)

        # uah-eur
        buy = response.xpath(
            """//table[@class="mb-table-currency"]/tbody/tr[1]/td[3]/text()"""
        ).extract_first()

        sell = response.xpath(
            """//table[@class="mb-table-currency"]/tbody/tr[2]/td[3]/text()"""
        ).extract_first()

        result = "UAH-EUR\nПокупка: {buy}\nПродажа: {sell}".format(
            buy=buy, sell=sell)
        result = urllib.quote(result)
        yield Request(self.url_to_send_message.format(result), dont_filter=True, callback=self.ok)

    def ok(self, response):
        yield {"ok": "ok"}
