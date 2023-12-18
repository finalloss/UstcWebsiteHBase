# 苏州高等研究院
# https://sz.ustc.edu.cn/
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
        nav_ul = soup.find('ul', {'class': 'c-b-line-1 n-ptb-5'})
        output_folder = 'outputCSV'
        os.makedirs(output_folder, exist_ok=True) 
        output_file_path = os.path.join(output_folder, 'file_list.csv')
        with open(output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Link', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            menu_items = nav_ul.find_all('li')
            count = 1
            for menu_item in menu_items:
                download_link = menu_item.find('a')['href']
                resource_center_url = base_url + download_link
                if count < 3:
                    print(download_link)
                    process_download_center(resource_center_url, writer)
                    count = count + 1
                    continue
                resource_center_response = requests.get(resource_center_url)
                resource_center_response.encoding='utf-8'
                resource_center_response.raise_for_status()
                time.sleep(1)  
                resource_center_soup = BeautifulSoup(resource_center_response.text, 'html.parser', from_encoding='utf-8')
                listright_div = resource_center_soup.find('ul', {'class': 'n-clear','id': 'company-tab'})
                list_items = listright_div.find_all('li')
                for item in list_items:
                    onclick_value = item.get('onclick')
                    if onclick_value:
                        link = onclick_value.split("'")[1]
                        resource_url = base_url + link
                        print(resource_url)
                        process_download_center(resource_url, writer)
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
def process_download_center(resource_center_url, writer):
    resource_center_response = requests.get(resource_center_url)
    resource_center_response.encoding='utf-8'
    resource_center_response.raise_for_status()
    time.sleep(1)  
    resource_center_soup = BeautifulSoup(resource_center_response.text, 'html.parser', from_encoding='utf-8')
    listright_div = resource_center_soup.find('ul', {'id': 'article_list_ul'})
    
    if listright_div:
        list_items = listright_div.find_all('li', {'class': 'n-bg-1 n-mb-1 c-border-2 n-pointer new-no-pic'})
        for item in list_items:
            title = item.find('h4', class_='n-e-1 n-f-3').text.strip()
            link = item.find('a')['href'].strip()
            date = item.find('span', class_='n-f-2 n-c-2 n-block n-text-right').text.strip()
            if not link.startswith('http'):
                link = base_url + link
            writer.writerow({'Title': title, 'Link': link, 'Time': date})

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    base_url = "https://sz.ustc.edu.cn"
    start_url = "/wdxz_list/98-1.html"
    crawl_website(base_url,start_url)
