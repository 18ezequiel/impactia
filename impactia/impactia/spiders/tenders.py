import scrapy
from impactia.items import ImpactiaItem
from scrapy.utils.project import get_project_settings
#from impactia.custome_exporters import CustomExporter

###########################################################################
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from scrapy.selector import Selector

###########################################################################


class TendersSpider(scrapy.Spider):

    def __init__(self, start_url=None, *args, **kwargs):
        super(TendersSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]

    name = "tenders"

    def parse(self,response):
        
        sel = Selector(response)
        url_caption = sel.xpath('//div[@id="body"]')


        ######### Raspado de data gruesa ##########
        next_url = response.xpath('//*[@id="cft.ojs.notice_link_0"]/@href').get() # Capturo el siguiente url para continuar el raspado
        title = response.xpath('//*[@id="cft_titleautolinked"]/text()').get()
        description = response.xpath('//*[@id="cft_descriptionautolinked"]/text()').get()
        procedure_type = response.xpath('//*[@id="cft.data.procedure_type"]/text()').get().replace("\n,\r,\t", "").strip()
        status = response.xpath('//*[@id="cft.data.status"]/text()').get().replace("\n,\r,\t", "").strip()
        nuts = response.xpath('//*[@id="cft.data.nuts"]/text()').get()
        main_cpv = response.xpath('//*[@id="cft.data.mainCpv.code"]/text()').get()
        total_value = response.xpath('//*[@id="cft.estimated.total.value"] /text()').get()
        

        # Guardo en un dicc
        meta_dict = {   "next_url": next_url , "title": title, 
                        "description": description, "procedure_type": procedure_type,
                        "status": status, "nuts": nuts, "main_cpv": main_cpv,
                        "total_value": total_value}
        yield scrapy.Request(next_url, callback=self.parse_1, meta=meta_dict)  # Pasar el diccionario como meta
    
    def parse_1(self, response):

        email_xpath1 = '//*[@id="fullDocument"]/div/div[3]/div[5]/div[1]/div/a[1]/text()'
        email_xpath2 = '//*[@id="fullDocument"]/div/div[3]/div[4]/div[1]/div/a[1]/text()'

        if all((email_xpath1, email_xpath2)):
            if response.xpath(email_xpath1).get():
                email_response = response.xpath(email_xpath1).get()
            else:
                email_response = response.xpath(email_xpath2).get()

        item = ImpactiaItem(
            # Recupero el dicc meta y defino item
            url = response.meta.get("next_url"),
            title = response.meta.get("title"),
            description = response.meta.get("description"),
            procedure_type = response.meta.get("procedure_type"),
            status = response.meta.get("status"),
            nuts = response.meta.get("nuts"),
            main_cpv = response.meta.get("main_cpv"),
            total_value = response.meta.get("total_value"),
            email = email_response)

        next_url = response.xpath('//*[@id="notice-tabs"]/li[2]/a/@href').get()
        next_url = f'https://ted.europa.eu/{next_url}'

        yield scrapy.Request(next_url, callback=self.parse_2, meta={'item': item})

    def parse_2(self, response):
        item = response.meta['item']
        language = response.css('table.data td:contains("Original language") + td::text').get()
        buyer = response.css('table.data td:contains("Country of the buyer") + td::text').get()
        document_sent = response.css('table.data td:contains("Document sent") + td::text').get()
        dead_line = response.css('table.data td:contains("Deadline for submission") + td::text').get()
        item['language'] = language.strip() if language else None
        item['buyer'] = buyer.strip() if buyer else None
        item['document_sent'] = document_sent.strip() if document_sent else None
        item['dead_line'] = dead_line.strip() if dead_line else None
        
        yield item


#scrapy crawl tenders -a start_url=https://etendering.ted.europa.eu/cft/cft-display.html?cftId=8832
#scrapy crawl tenders -a start_url=https://etendering.ted.europa.eu/cft/cft-display.html?cftId=8832 -s FEED_EXPORT_HEADERS=False
