# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst
import scrapy

def convert_number(value):
    value = value.replace(' ', '')
    try:
        value = int(value)
    except:
        try:
            value = float(value)
        except:
            return value
        return value
    return value

def clean_str(value):
    pass

class LeroyparsItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert_number), output_processor=TakeFirst())
    specifications_name = scrapy.Field(input_processor=MapCompose(lambda x: x.strip('\n '), convert_number))
    specifications_values = scrapy.Field(input_processor=MapCompose(lambda x: x.strip('\n '), convert_number))
    specifications = scrapy.Field()
