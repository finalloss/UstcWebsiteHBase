# 大数据学院
# http://sds.ustc.edu.cn
import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import warnings
def crawl_website(base_url, start_url):
    url = base_url + start_url
    try:
        response = requests.get(url)
        response.encoding='utf-8'
        response.raise_for_status()  # 检查请求是否成功
        time.sleep(1)  # 在这里设置延迟时间，单位为秒
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
        resource_center_tag = soup.find('a', {'title': '资源中心'})
        resource_center_url = resource_center_tag['href'] if resource_center_tag else None
        if resource_center_url:
            resource_center_url = base_url + resource_center_url
            print(resource_center_url)
            process_download_center(resource_center_url)
        else:
            print("未找到资源中心链接")
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")

def process_download_center(resource_center_url):
    resource_center_response = requests.get(resource_center_url)
    resource_center_response.encoding='utf-8'
    resource_center_response.raise_for_status()
    time.sleep(1)  
    resource_center_soup = BeautifulSoup(resource_center_response.text, 'html.parser', from_encoding='utf-8')
    listright_div = resource_center_soup.find('ul', {'class': 'wp_article_list'})
    list_items = listright_div.find_all('li')
    output_folder = 'outputCSV'
    os.makedirs(output_folder, exist_ok=True) 
    output_file_path = os.path.join(output_folder, 'file_list.csv')
    with open(output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Link', 'Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for item in list_items:
            title = item.find('span', class_='Article_Title').text.strip()
            link = item.find('a')['href'].strip()
            date = item.find('span', class_='Article_PublishDate').text.strip()
            if not link.startswith('http'):
                link = base_url + link
            writer.writerow({'Title': title, 'Link': link, 'Time': date})

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    base_url = "http://sds.ustc.edu.cn"
    start_url = "/main.htm"
    crawl_website(base_url,start_url)
