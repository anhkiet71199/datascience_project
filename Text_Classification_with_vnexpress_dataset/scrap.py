from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm
import re
import random
import shutil
import pandas as pd

def scrap(page, categories, path):
    main_url = 'https://vnexpress.net'
    for category in categories:
        create_folder(category, path)
        global count
        count = 1
        sub_class = ''.join(category.split('-'))
        path_main_category = os.path.join(path, category)
        url_category = main_url + '/' + category
        sub_category = category

        # Scrap main category
        scrap_page(url_category, path_main_category, category, sub_category)
        for i in range(1,page):
            soup = get_soup(url_category)
            try:
                next_page = list(soup.find('a', class_='btn-page next-page').get('href'))
                next_page.remove('/')
                next_page = ''.join(next_page)
                url_category = main_url + '/'+ next_page
                scrap_page(url_category, path_main_category, category, sub_category)
            except:
                pass
        
        # Scrap sub category
        soup = get_soup(url_category)
        a_tags = soup.find_all('a')
        pattern = re.compile(r"^"+ "/" + category + "/"+".*$")
        for a in a_tags:
            href_value = a.get('href')
            if href_value and pattern.match(href_value):
                sub_category_href = href_value
                parts = sub_category_href.split('/')
                sub_category = parts[-1]
                sub_url_category = main_url + sub_category_href
                scrap_page(sub_url_category, path_main_category, category, sub_category)
                for i in range(1, page):
                    soup = get_soup(sub_url_category)
                    try:
                        next_page = list(soup.find('a', class_='btn-page next-page').get('href'))
                        next_page.remove('/')
                        next_page = ''.join(next_page)
                        sub_url_category = main_url + '/'+ next_page
                        scrap_page(sub_url_category, path_main_category, category, sub_category)
                    except:
                        pass

def scrap_page(url, path_, category, sub_category):
    global count
    soup = get_soup(url)
    all_news = soup.find_all(class_='title-news')
    for i in tqdm(range(len(all_news)), desc=sub_category):
        try:
            link_news = all_news[i].find('a').get('href')
            file_name = link_news.rsplit('/', 1)[-1]
            file_name = file_name.replace('.html', '')
            title = all_news[i].find('a').get('title')
            file = path_ + '\\'+ file_name + '.txt'
            scrap_to_file(link_news,file)
            count += 1
        except:
            pass


def scrap_to_file(link_news, file):
    soup = get_soup(link_news)
    try:
        date = soup.find('span', class_='date').text
        title = soup.find('h1',class_='title-detail').text
        description = soup.find('p', class_='description').text
        text_normal = soup.find_all('p', class_='Normal')
        with open(file, 'w',encoding='utf-8') as f:
            f.write(date+'\n')
            f.write(title+'\n')
            f.write(description+'\n')
            for text in text_normal:
                f.write(text.text+'\n')
    except:
        pass

# BeautifulSoup
def get_soup(url):
    response = requests.get(url)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

# Create folder to hold file scrap
def create_folder(category, path):
    path_category = os.path.join(path, category)
    os.makedirs(path_category, exist_ok=True)


# Divide train and test folder
def split_train_test_folder(source_path, train_path, test_path, categories, train_ratio):
    for folder in categories:
        files = os.listdir(os.path.join(source_path, folder))
        num_files = len(files)
        num_train = int(train_ratio * num_files)
        random.shuffle(files)

        train_files = files[:num_train]
        test_files = files[num_train:]

        path_train_category = os.path.join(train_path, folder)
        os.makedirs(path_train_category, exist_ok=True)
        path_test_category = os.path.join(test_path, folder)
        os.makedirs(path_test_category, exist_ok=True)

        for file_name in train_files:
            source_file = os.path.join(source_path, folder, file_name)
            target_file = os.path.join(train_path, folder, file_name)
            shutil.copy(source_file, target_file)

        for file_name in test_files:
            source_file = os.path.join(source_path, folder, file_name)
            target_file = os.path.join(test_path, folder, file_name)
            shutil.copy(source_file, target_file)

# Create file csv to train and test
def read_file_create_csv(path, categories, path_csv):
    data = []
    for label in os.listdir(path):
        label_path = os.path.join(path, label)
        if os.path.isdir(label_path):
            for file_name in os.listdir(label_path):
                file_path = os.path.join(label_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    if len(lines) > 1:  
                        content = ''.join(lines[1:])
                        data.append([content, label])

    df = pd.DataFrame(data, columns=['content', 'label'])
    df.to_csv(path_csv, index=False)


if __name__ == "__main__":
    # Category-label for data
    categories = [ 'thoi-su', 'the-gioi', 'kinh-doanh', 'bat-dong-san', \
    'khoa-hoc', 'giai-tri',  'the-thao', 'phap-luat', 'giao-duc',  'suc-khoe', 'doi-song', 'du-lich', 'so-hoa']
    dir_path = os.getcwd()

    # Folder raw data
    path_scrap = os.path.join(dir_path, 'scrap_raw_data')
    os.makedirs(path_scrap, exist_ok=True)

    # Crawl data
    scrap(20, categories, path_scrap)

    # Divide train_test data
    path_dataset = os.path.join(dir_path, 'dataset')
    os.makedirs(path_dataset, exist_ok=True)
    train_ratio = 0.8
    train_path = os.path.join(path_dataset,'train')
    test_path = os.path.join(path_dataset, 'test')

    os.makedirs(train_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)

    # split to train and test folder
    split_train_test_folder(path_scrap, train_path, test_path, categories, train_ratio)
    path_train_csv = os.path.join(path_dataset, 'train.csv')
    path_test_csv = os.path.join(path_dataset, 'test.csv')

    # To CSV file
    read_file_create_csv(train_path, categories, path_train_csv)
    read_file_create_csv(test_path, categories, path_test_csv)
