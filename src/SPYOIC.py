# 国合部
# https://oic.ustc.edu.cn
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
    listright_div = resource_center_soup.find('div', {'class': 'post_type_list'})
    pageTurn_ul = resource_center_soup.find('div', {'class': 'pagination'})
    list_items = listright_div.find_all('article')
    
    for item in list_items:
        title = item.find('div', class_='title').text.strip()
        link = item.find('a')['href'].strip()
        date = item.find('div', class_='date').text.strip()
        match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date)
        if match:
            year, month, day = match.groups()
            formatted_time = f'{year}-{month.zfill(2)}-{day.zfill(2)}'
        if not link.startswith('http'):
            link = base_url + link
        writer.writerow({'Title': title, 'Link': link, 'Time': formatted_time})
    linkdiv = pageTurn_ul.find('a', {'class': 'next page-numbers'})
    if linkdiv:
        link = linkdiv['href'].strip()
        print(link)
        process_download_center(link, writer)

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    base_url = "https://oic.ustc.edu.cn"
    start_url = "/download/"
    crawl_website(base_url,start_url)
