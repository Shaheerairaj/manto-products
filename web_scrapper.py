import os
import pandas as pd
import requests
import bs4
import lxml
from datetime import datetime
import requests
import bs4
import csv

import logging
import warnings
warnings.filterwarnings("ignore")


# Function to scrape and save data for a given URL and category
def scrape_and_save(url, category, data_dict):
    page_number = 1

    while True:
        current_url = url.format(page_number)
        r = requests.get(current_url)
        
        # Check if the request was successful
        if r.status_code != 200:
            print(f"Failed to retrieve page {page_number} for {category}. Exiting.")
            break

        s = bs4.BeautifulSoup(r.text, 'lxml')

        # Check if there are no products on the page
        products = s.find(id="root").select('.product-item__meta')
        if not products:
            print(f"No products found on page {page_number} for {category}. Exiting.")
            break

        # Iterate through all products on the page
        for i, product in enumerate(products):
            product_name = product.select('a')[0].text
            product_price = s.find(id="root").select('.product-item__price')[i].text.replace('\n', '')

            # Store the data in the dictionary
            data_dict.append({'Category': category, 'Product': product_name, 'Price': product_price})

        # Move on to the next page
        page_number += 1



url = "https://www.manto.ae/collections/manto-men"

r = requests.get(url)
s = bs4.BeautifulSoup(r.text, 'lxml')


# List of URLs and categories
urls_and_categories = [
    {"url": "https://www.manto.ae/collections/manto-men?page={}", "category": "Men"},
    {"url": "https://www.manto.ae/collections/best-seller-women?page={}", "category": "Women"}
]

# List to store data
data_list = []

# Scrape data for each URL and category
for item in urls_and_categories:
    scrape_and_save(item["url"], item["category"], data_list)

# Save data to CSV
file_date = str(datetime.now().date())
csv_file_path = f"Data/data_export_{file_date}.csv"
fields = ['Category', 'Product', 'Price']

with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data_list)

print(f"Data has been saved to {csv_file_path}.")