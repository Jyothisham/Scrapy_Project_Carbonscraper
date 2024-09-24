
import scrapy
from scrapy import Spider
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Carbon38Spider(Spider):
    name = "carbon38"
    start_urls = ['https://carbon38.com/collections/tops']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')
        product_urls = response.xpath('//a[@class="product-item-link"]/@href').extract()
        for url in product_urls:
            yield scrapy.Request(url, callback=self.parse_product)

        next_page = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_product(self, response):
        yield {
            'breadcrumbs': response.xpath('//div[@class="breadcrumbs"]//text()').extract(),
            'primary_image_url': response.xpath('//img[@class="primary-image"]/@src').extract_first(),
            'brand': response.xpath('//span[@class="brand"]//text()').extract_first(),
            'product_name': response.xpath('//h1[@class="product-name"]//text()').extract_first(),
            'price': response.xpath('//span[@class="price"]//text()').extract_first(),
            'reviews': response.xpath('//span[@class="reviews"]//text()').extract_first(),
            'colour': response.xpath('//span[@class="color"]//text()').extract_first(),
            'sizes': response.xpath('//span[@class="size"]//text()').extract(),
            'description': response.xpath('//div[@class="description"]//text()').extract_first(),
            'sku': response.xpath('//span[@class="sku"]//text()').extract_first(),
            'product_id': response.xpath('//span[@class="product-id"]//text()').extract_first(),
            'product_url': response.url,
            'image_urls': response.xpath('//img[@class="additional-image"]/@src').extract(),
        }

    def closed(self, reason):
        self.driver.quit()





