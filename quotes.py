import os
import csv
import requests
import random
import pandas as pd
from bs4 import BeautifulSoup
from constants import Constants
const = Constants()

def get_the_quote(emotion):
    """
    Returns a quote that belongs to the emotion that is passed and is chosen at random from the csv 
    file containing a number of quottes per emotion.

    Args:
    
    emotion- a string depecting an emotion. The quote returned by the function is of this type.

    Returns:
    
    A quote of the emotion type passed.  
    """
    quote_list = []
    with open(const.clustered_quotes) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[1] == emotion:
                quote_list.append(row[2])

    print (quote_list)
    return (quote_list)


def fetch_quotes():
        """
        Creates a dataset of quotes for different emotions
        """
        if not os.path.exists(const.clustered_quotes):
            quotes_dataframe = pd.DataFrame(columns=['emotion','quote'])

            url = const.quotes_url
            emotions = const.quotes_emotions_mapping.values()
            i=0

            for emotion in emotions:
                print(emotion)
                source_code=requests.get(url + emotion)
                plain_text=source_code.text
                soup=BeautifulSoup(plain_text, "html.parser")
                list_items = soup.findAll('div')
                for div in list_items:
                    for a in div.find_all('a', title="view quote"):
                        if a.get('class') != ['oncl_q'] and not(quotes_dataframe['quote']==a.text).any():
                            quotes_dataframe.loc[i]=[emotion, a.text]
                            i=i+1

            quotes_dataframe.to_csv(const.clustered_quotes, encoding='utf-8')

