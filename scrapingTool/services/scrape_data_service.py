import json
import os

import requests
from retrying import retry
from typing import List

import constants
from utils.make_requests import Requests
from bs4 import BeautifulSoup


class ScrapingTool:

    def __init__(self):
        self.cache = {}
        ##Below steps are done to mock in-mempory db
        if os.path.exists('scraped_data.json'):
            with open('scraped_data.json', 'r') as f:
                try:
                    data = json.load(f)
                    for item in data:
                        product_title = item.get('product_title')
                        self.cache[product_title] = {
                            'product_price': item.get('product_price'),
                        }
                except json.JSONDecodeError as e:
                    print(f"Error loading scraped_data.json: {e}")

    @retry(wait_fixed=2000, stop_max_attempt_number=3)  # Retry 3 times with a fixed delay of 2 seconds
    def fetch_page(self, page:int, proxy:str=None):
        response = Requests().make_request("GET", constants.scrape_url, f"page/{page + 1}", {},
                                           proxies={'https': proxy})
        response.raise_for_status()
        return response

    def scrape_data(self, page_limit=1, proxy=None):
        response_data = {
            "scrapedData": [],
            "updatedData": []
        }
        scraped_data = []
        updated_data = []
        for page in range(page_limit):
            try:
                response = self.fetch_page(page, proxy)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    products = soup.find_all('li', class_='type-product')
                    for product in products:
                        product_name = product.find('h2', class_='woo-loop-product__title').text.strip()
                        product_price = float(
                            product.find('span', class_='woocommerce-Price-amount amount').text.strip().replace('₹', ''))
                        image_url = product.find('img')['src']
                        product_data = {
                            'product_title': product_name,
                            'product_price': product_price,
                            'path_to_image': image_url
                        }
                        scraped_data.append(product_data)
                        if self.should_update_cache(product_name, product_price):
                            self.cache[product_name] = product_data
                            updated_data.append(product_data)
            except (requests.RequestException, ValueError) as e:
                print(f"Error scraping page {page}: {e}")
        response_data["scrapedData"] = scraped_data
        response_data["updatedData"] = updated_data
        return response_data

    def should_update_cache(self, product_name: str, new_price: float) -> bool:
        if product_name in self.cache:
            current_price = self.cache[product_name]['product_price']
            return new_price != current_price
        return True

    def save_to_json(self, data: List[dict], file_path: str):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def notify_status(self, num_scraped: int, num_updated: int):
        print(f"Scraping Status: {num_scraped} products scraped, {num_updated} products updated in DB")

