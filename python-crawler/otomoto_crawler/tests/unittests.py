import unittest
from scrapy.http import HtmlResponse
from otomoto_crawler.tests.test_data import *
from otomoto_crawler.spiders.car_spider import CarSpider

class TestCarSpider(unittest.TestCase):

    def test_parse_car_common(self):
        response = HtmlResponse(url="https://www.otomoto.pl/osobowe/oferta/bmw-seria-3-325i-sedan-manual-z-niemiec-rakieta-ID6G5Td5.html", body=SAMPLE_HTML1, encoding="utf-8")

        spider = CarSpider()

        results = list(spider.parse_car(response))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["brand"], "BMW")
        self.assertEqual(results[0]["year"], "2005")
        self.assertEqual(results[0]["mileage"], "279 000 km")
        self.assertEqual(results[0]["capacity"], "2 497 cm3")
        self.assertEqual(results[0]["horse_power"], "218 KM")
        self.assertEqual(results[0]["fuel_type"], "Benzyna")
        self.assertEqual(results[0]["transmission"], "Manualna")
        self.assertEqual(results[0]["number_of_doors"], "5")
        self.assertEqual(results[0]["color"], "Czarny")
        self.assertEqual(results[0]["is_used"], "Używane")
        self.assertEqual(results[0]["price"], "16 500")
    
    def test_parse_car_country(self):
        
        response = HtmlResponse(url="https://www.otomoto.pl/osobowe/oferta/opel-corsa-opel-corsa-c-1-0-automat-ID6G4FeF.html", body=SAMPLE_HTML2, encoding="utf-8")

        spider = CarSpider()

        results = list(spider.parse_car(response))

        self.assertEqual(results[0]["origin_country"], "Niemcy")  

    def test_parse_car_aso(self):

        response = HtmlResponse(url="https://www.otomoto.pl/osobowe/oferta/opel-corsa-opel-corsa-c-1-0-automat-ID6G4FeF.html", body=SAMPLE_HTML2, encoding="utf-8")

        spider = CarSpider()

        results = list(spider.parse_car(response))

        self.assertEqual(results[0]["aso"], "Tak")

    def test_parse_car_no_accidents(self):

        response = HtmlResponse(url="https://www.otomoto.pl/osobowe/oferta/cupra-formentor-2-0-tsi-190-km-4x4-7-automat-dsg-xl-el-klapa-kola-19-kamera-360-ID6G4Frq.html", body=SAMPLE_HTML3, encoding="utf-8")

        spider = CarSpider()

        results = list(spider.parse_car(response))

        self.assertEqual(results[0]["no_accidents"], "Tak")

if __name__ == "__main__":
    unittest.main()