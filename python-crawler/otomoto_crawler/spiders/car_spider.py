import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from otomoto_crawler.items import CarCrawlerItem


class CarItemLoader(ItemLoader):
    default_item_class = CarCrawlerItem
    default_output_processor = TakeFirst()


class CarSpider(scrapy.Spider):
    name = "car-spider"
    allowed_domains = ["otomoto.pl"]
    base_url = "https://www.otomoto.pl/osobowe/"
    start_urls = [base_url]

    def parse(self, response):
        page_number = response.xpath(
            '//li[contains(@class, "pagination-item")][position()=last()-1]//span/text()'
        ).get()
        # some weird bug: otomoto shows more that 500 pages, but when u try to access
        # them it redirects u to the page 500
        page_number = min(1, int(page_number))
        for page in range(1, page_number+1):
            yield scrapy.Request(
                url=f"{self.base_url}?page={page}",
                callback=self.parse_page,
            )

    def parse_page(self, response):
        car_links = response.css(
            "div[data-testid='search-results'] article h1 a::attr(href)"
        ).getall()
        car_links = filter(
            lambda link: link.startswith(f"{self.base_url}oferta"), car_links
        )
        car_links = list(set(car_links))
        for link in car_links:
            yield scrapy.Request(url=link, callback=self.parse_car)

    def parse_car(self, response):
        features_map = {
            "Marka pojazdu": "brand",
            "Rok produkcji": "year",
            "Przebieg": "mileage",
            "Pojemność skokowa": "capacity",
            "Moc": "horse_power",
            "Rodzaj paliwa": "fuel_type",
            "Skrzynia biegów": "transmission",
            "Liczba drzwi": "number_of_doors",
            "Kraj pochodzenia": "origin_country",
            "Kolor": "color",
            "Bezwypadkowy": "no_accidents",
            "Serwisowany w ASO": "aso",
            "Stan": "is_used",
        }

        loader = CarItemLoader(response=response)

        features = response.css("[data-testid='advert-details-item']")
        for feature in features:
            feature_name = feature.css("p::text").extract_first().strip()
            if feature_name in features_map:
                feature_value = feature.css(":last-child::text").extract_first().strip()
                loader.add_value(features_map[feature_name], feature_value)

        price = response.css(".offer-price__number::text").extract_first().strip()
        loader.add_value("price", price)

        yield loader.load_item()
