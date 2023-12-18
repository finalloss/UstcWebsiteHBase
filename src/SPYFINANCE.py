# 财务处
# https://finance.ustc.edu.cn/
import requests
import re
from bs4 import BeautifulSoup
import csv
import time
import os
import math
import warnings

def crawl_website(base_url, start_url):
    url = base_url + start_url
    try:
        output_folder = 'outputCSV'
        os.makedirs(output_folder, exist_ok=True) 
        output_file_path = os.path.join(output_folder, 'file_list.csv')
        with open(output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Link', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            print(url)
            process_download_center(url, writer)  
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")

def process_download_center(resource_center_url, writer):
    resource_center_response = requests.get(resource_center_url)
    resource_center_response.encoding='utf-8'
    resource_center_response.raise_for_status()
    time.sleep(1)  
    resource_center_soup = BeautifulSoup(resource_center_response.text, 'html.parser', from_encoding='utf-8')
    listright_div = resource_center_soup.find('ul', {'class': 'news_list list2'})
    pageTurn_ul = resource_center_soup.find('li', {'class': 'page_nav'})
    list_items = listright_div.find_all('li')
    
    for item in list_items:
        title = item.find('span', class_='news_title').text.strip()
        link = item.find('a')['href'].strip()
        date = item.find('span', class_='news_meta').text.strip()

        if not link.startswith('http'):
            link = base_url + link
        writer.writerow({'Title': title, 'Link': link, 'Time': date})
    linkdiv = pageTurn_ul.find('a', {'class': 'next'})['href'].strip()
    if not linkdiv == 'javascript:void(0);':
        llink = base_url + linkdiv
        print(llink)
        process_download_center(llink, writer)

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    base_url = "https://finance.ustc.edu.cn"
    start_url = "/xzzx/list.psp"
    crawl_website(base_url,start_url)
