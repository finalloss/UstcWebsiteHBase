# 网络安全学院
# https://cybersec.ustc.edu.cn
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
        nav_ul = soup.find('ul', {'class': 'w cle'})
        output_folder = 'outputCSV'
        os.makedirs(output_folder, exist_ok=True) 
        output_file_path = os.path.join(output_folder, 'file_list.csv')
        with open(output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Link', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            menu_items = nav_ul.find_all('li', {'class': re.compile(r'fl*?')})
            for menu_item in menu_items:
                sub_menu = menu_item.find('dl')
                if sub_menu:
                    li_items = sub_menu.find_all('dd')
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
    listright_div = resource_center_soup.find('div', {'id': 'wp_news_w50'})
    if listright_div:
        list_items = listright_div.find_all('li', {'class': 'cle'})
        for item in list_items:
            title = item.find('div', class_='fl text txtov').text.strip()
            link = item.find('a')['href'].strip()
            date = item.find('div', class_='fr time').text.strip()
            match = re.search(r'\d{4}-\d{1,2}-\d{1,2}', date)
            if match:
                extracted_time = match.group()
            if not link.startswith('http'):
                link = base_url + link
            writer.writerow({'Title': title, 'Link': link, 'Time': extracted_time})

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    base_url = "https://cybersec.ustc.edu.cn"
    start_url = "/main.htm"
    crawl_website(base_url,start_url)
