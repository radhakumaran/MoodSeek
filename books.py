from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import pandas as pd
import bs4
import os
import urllib
from time import sleep
from sklearn.cluster import KMeans
from constants import Constants

const = Constants()
def getBookDescription():
    """
    Scrapes data of books from Goodreads and creates the dataset
    """
    
    # to avoid unicode errors (run on terminal) - chcp 65001
    list_df=[]
    url_list = []
    
    url = const.book_url

    r = requests.get(url)    
    bs = bs4.BeautifulSoup(r.text, features="lxml")
    for link in bs.findAll('a', attrs={'class': 'bookTitle'},  href=True):
        url_list.append("https://www.goodreads.com/"+ link["href"])

    del url_list[93:]
    del url_list[9]
    del url_list[7]
    image_dir = const.books_image_dir


    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    print (len(url_list))
    i = 0
    for record in url_list:
        sleep(10)
        print ('\n', i, '\n')
        i+=1
        r2 = requests.get(record)
        bs2 = bs4.BeautifulSoup(r2.text, features="lxml")
        for movie, img in zip(bs2.findAll('div', attrs={'id': 'metacol'}), bs2.findAll('div', attrs={'id': 'imagecol'})):
            title = movie.find('h1', attrs={'id': 'bookTitle'}).get_text()
            title = title.encode('ascii', errors = 'ignore').strip().decode()
            print (title)
            author = movie.find('span', attrs={'itemprop': 'name'}).get_text()
            print (author)
            
            
            image = img.find('img', id='coverImage')
            print (image)
            save_dir = image_dir + "/" + title.replace(' ', '%20') + '_' + author.replace(' ', '%20')
            urllib.request.urlretrieve(image['src'], save_dir)
            description = movie.find('div', attrs={'id': 'description'}).find('span', {'style': 'display:none'})
            if description == None:
                description = movie.find('div', attrs={'id': 'description'}).get_text()
            else :
                description = description.get_text()
            print (description)
            list_df.append([title, author, description, save_dir])
    df = pd.DataFrame(list_df,columns=['Title','Author', 'Description', 'Image'])
    df.to_csv(const.book_dataset, encoding='utf-8')
    


def getTextSentiment(message_text):
    """
    Identifies the sentiment expressed by a piece of text.

    Args:

    message_text: the piece of text whose sentiment is to be analysed

    Returns:

    The sentiment polarity score of the text
    """
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(message_text)

    return scores

def Clustering():
    """
    Classifies the dataset of books based on the emotion they express, as identified from their summaries.

    """
    df= pd.read_csv(const.book_dataset, sep=',', encoding='utf-8')
    list_df=[]
    for item in df["Description"]:
        list_df.append(getTextSentiment(item))
    X = pd.DataFrame(list_df)
    kmeans = KMeans(n_clusters=7)
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)
    centers = kmeans.cluster_centers_
    list_emotions=const.user_emotions
    list_pred_emotions=[]
    centers_sorted=sorted(centers,key=lambda l:l[0])
    for value in y_kmeans:
        list_pred_emotions.append(list_emotions[value])
    df["Emotion"]=list_pred_emotions
    df.to_csv(const.clustered_books, sep=',', encoding='utf-8', index = False)
    
    


def books_classify():
    """
    Creates the book dataset and classifies them, if not already done
    """
    if not os.path.exists(const.book_dataset):
        getBookDescription() 
    if not os.path.exists(const.clustered_books):
        Clustering()


def get_books(emotion):
    """
    Returns a set of books for a given emotion.

    Args:

    emotion: The emotion for which you want books to be fetched.

    Returns:

    The set of books for the particular emotion
    """
    df = pd.read_csv(const.clustered_books)
    df = df.loc[df.Emotion == emotion]
    return df.sample(const.book_num)

