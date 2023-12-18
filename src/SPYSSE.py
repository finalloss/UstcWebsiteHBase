# 软件学院
# https://sse.ustc.edu.cn/
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
        response = requests.get(url, verify=False, headers={'Connection':'close'})
        requests.adapters.DEFAULT_RETRIES = 5
        response.encoding='utf-8'
        response.raise_for_status()  
        time.sleep(1)  
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
        nav_ul = soup.find('ul', {'class': 'wp_listcolumn'})
        output_folder = 'outputCSV'
        os.makedirs(output_folder, exist_ok=True) 
        output_file_path = os.path.join(output_folder, 'file_list.csv')
        with open(output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Link', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            menu_items = nav_ul.find_all('li', {'class': re.compile(r'wp_column column-*?')})
            for menu_item in menu_items:
                download_link = menu_item.find('a')['href']
                resource_center_url = base_url + download_link
                print(resource_center_url)
                process_download_center(resource_center_url, writer)
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")

def process_download_center(resource_center_url, writer):
    resource_center_response = requests.get(resource_center_url)
    resource_center_response.encoding='utf-8'
    resource_center_response.raise_for_status()
    time.sleep(1)  
    resource_center_soup = BeautifulSoup(resource_center_response.text, 'html.parser', from_encoding='utf-8')
    listright_div = resource_center_soup.find('ul', {'class': 'wp_article_list'})
    pageTurn_ul = resource_center_soup.find('ul', {'class': 'wp_paging clearfix'})
    
    if pageTurn_ul:
        list_items = listright_div.find_all('li', {'class': re.compile(r'list_item i*?')})
        pageTurn_li = pageTurn_ul.find('li', {'class': 'page_nav'})
        
        for item in list_items:
            title = item.find('span', class_='Article_Title').text.strip()
            link = item.find('a')['href'].strip()
            date = item.find('span', class_='Article_PublishDate').text.strip()
            if not link.startswith('http'):
                link = base_url + link
            writer.writerow({'Title': title, 'Link': link, 'Time': date})
        link = pageTurn_li.find('a', {'class': 'next'})['href'].strip()
        if not link == 'javascript:void(0);':
            resource_url = base_url + link
            print(resource_url)
            process_download_center(resource_url, writer)


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    base_url = "https://sse.ustc.edu.cn"
    start_url = "/wdxz_19877/list.htm"
    crawl_website(base_url,start_url)
