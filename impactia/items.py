# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImpactiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    language = scrapy.Field()
    email = scrapy.Field()
    description = scrapy.Field()
    procedure_type = scrapy.Field()
    status = scrapy.Field()
    nuts = scrapy.Field()
    main_cpv = scrapy.Field()
    total_value = scrapy.Field()
    buyer = scrapy.Field()
    document_sent = scrapy.Field()
    dead_line = scrapy.Field()


