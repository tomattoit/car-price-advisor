import scrapy


class CarCrawlerItem(scrapy.Item):
    brand = scrapy.Field(default=None)
    price = scrapy.Field(default=None)
    year = scrapy.Field(default=None)
    mileage = scrapy.Field(default=None)
    capacity = scrapy.Field(default=None)
    horse_power = scrapy.Field(default=None)
    fuel_type = scrapy.Field(default=None)
    transmission = scrapy.Field(default=None)
    number_of_doors = scrapy.Field(default=None)
    color = scrapy.Field(default=None)
    origin_country = scrapy.Field(default=None)
    no_accidents = scrapy.Field(default=None)
    aso = scrapy.Field(default=None)
    is_used = scrapy.Field(default=None)
