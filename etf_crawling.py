import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from time import time, sleep
import pathlib
import matplotlib.pyplot as plt
import numpy as np
from random import randint


def get_info_from_betashares(soup):
    """ Crawl date and last trade value from betaShares """
    info = soup.find_all("span", {"class": "dt"})
    date = info[0].get_text()
    date = date.split(' ')[0] + ' ' + date.split(' ')[1][:3] + ' ' + date.split(' ')[2]
    date = datetime.datetime.strptime(date, "%d %b %Y").strftime("%d-%m-%Y")
    info = soup.find_all("td", {"class": "w20"})
    last_trade = info[4].get_text()
    last_trade = last_trade.replace('$', '')
    return date, last_trade
   
def get_info_from_ishares(soup):
    """ Crawl date and last trade value from iShares """
    info = soup.find_all("span", {"class": "header-nav-label navAmount"})
    date = info[0].get_text()
    date = date.split(' ')[3]
    date = date.replace('\n', '')
    date = date.replace('-', ' ')
    date = datetime.datetime.strptime(date, "%d %b %Y").strftime("%d-%m-%Y")
    info = soup.find_all("span", {"class": "header-nav-data"})
    last_trade = info[0].get_text()
    last_trade = last_trade.replace('\n', '')
    last_trade = last_trade.replace('AUD ', '')
    return date, last_trade


def add_new_record(df, betashares, ishares):
    """ 
        store crawled information to new column and save in DF 
    """
    record = []
    for etf in betashares:
        url = 'https://www.betashares.com.au/fund/{}/'.format(betashares[etf])
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        date, last_trade = get_info_from_betashares(soup)
        record.append(last_trade)

    for etf in ishares:
        url = 'https://www.blackrock.com/au/individual/products/{}'.format(ishares[etf])
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        date, last_trade = get_info_from_ishares(soup)
        record.append(last_trade)
    print("Date: {} has beed added to records".format(date))
    # add new column to the DF
    df[date] = record
    return df


def read_records(RECORD_FILE):
    """
        Read record file in directory
    """
    file = pathlib.Path(RECORD_FILE)
    if file.exists():
        df = pd.read_csv(RECORD_FILE, sep=',', encoding='utf-8')
        print("{} is exist, we load the exist file".format(RECORD_FILE))
    else:
        df = pd.DataFrame(columns=['ETFs'])
        etf_list = ['Tech Savvy', 'Sustainability Leaders', 'Aussie Top 200', 'Global 100', 'Emerging Markets', 'Health Wise']
        df['ETFs'] = etf_list
        print("{} is not exist, we create a new file".format(RECORD_FILE))
    return df


# show records
def show_records(new_df):
    # set colors
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    
    # set x-axis
    date = list(new_df.columns)
    date.remove('ETFs')
    x = date
    # set figure size
    plt.figure(figsize=(12, 8), dpi=80)
    # set label
    plt.title('ETFs trend records', fontsize=18)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('$ Dollar', fontsize=16)
    # multiple line plots
    for i in range(len(new_df)):
        y = new_df[date].iloc[i].values
        plt.plot(x, y, color=colors[i], marker='o', markersize=8, label=new_df['ETFs'].iloc[i])
    
        for i, value in enumerate(y):
            plt.text(i, round(float(value), 0), value, fontsize=12)

    plt.tight_layout()
    # show legend
    plt.legend(loc='upper right')

    plt.savefig('img/ETF_trends.pdf', bbox_inches='tight')

    return plt


def etf_crawling(RECORD_FILE, betashares, ishares):
	# read record
    df = read_records(RECORD_FILE)
    # update records
    records = add_new_record(df, betashares, ishares) 
    # visualize the records
    show_records(records)
    # save the record
    records.to_csv(RECORD_FILE, sep=',', encoding='utf-8', index=False)



