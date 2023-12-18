# 信息科学技术学院
# https://sist.ustc.edu.cn
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
        nav_ul = soup.find('ul', {'class': 'py-3 pb-4'})
        output_folder = 'outputCSV'
        os.makedirs(output_folder, exist_ok=True) 
        output_file_path = os.path.join(output_folder, 'file_list.csv')
        with open(output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Link', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            menu_items = nav_ul.find_all('li', {'class': 'dropdown'})
            for menu_item in menu_items:
                sub_menu = menu_item.find('ul')
                if sub_menu:
                    li_items = sub_menu.find_all('li')
                    for li_item in li_items:
                        if '资料下载' in li_item.text:
                            download_link = li_item.find('a')['href']    
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
    listright_div = resource_center_soup.find('div', {'class': 'row gy-4'})
    pageTurn_ul = resource_center_soup.find('ul', {'class': 'wp_paging clearfix'})
    
    if pageTurn_ul:
        list_items = listright_div.find_all('div', {'class': 'col-xl-4 col-md-6'})
        pageTurn_li = pageTurn_ul.find('li', {'class': 'page_nav'})
        
        for item in list_items:
            card = item.find('div', {'class': 'card-body'})
            title = card.find('h5', class_='card-title fs-semibold text-truncate').text.strip()
            link = card.find('a')['href'].strip()
            date = card.find('time').text.strip()
            match = re.search(r'\d{4}-\d{2}-\d{2}', date)
            if match:
                extracted_time = match.group()
            if not link.startswith('http'):
                link = base_url + link
            writer.writerow({'Title': title, 'Link': link, 'Time': extracted_time})
        link = pageTurn_li.find('a', {'class': 'next'})['href'].strip()
        if not link == 'javascript:void(0);':
            resource_url = base_url + link
            print(resource_url)
            process_download_center(resource_url, writer)
    else: 
        listright_div = resource_center_soup.find('div', {'class': 'paging_content', 'id': 'wp_content_w6_0'})
        list_items = listright_div.find_all('p')
        for item in list_items:
            title = item.find('a').text.strip()
            link = item.find('a')['href'].strip()
            if not link.startswith('http'):
                link = base_url + link
            writer.writerow({'Title': title, 'Link': link})

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    base_url = "https://sist.ustc.edu.cn"
    start_url = "/main.htm"
    crawl_website(base_url,start_url)
