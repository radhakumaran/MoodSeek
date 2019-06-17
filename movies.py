from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import pandas as pd
import bs4
import os
import urllib
from time import sleep
from constants import Constants
from sklearn.cluster import KMeans

const = Constants()


def getMovieDescription():
    """
    Extracts details of the top feature films from the IMDb website and stores them in a CSV file.

    """
    
    list_df=[]

    image_dir = const.movies_image_dir


    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    url = const.movies_url
    r = requests.get(url)    
    bs = bs4.BeautifulSoup(r.text, features="lxml")
    for movie in bs.findAll('div', attrs={'class': 'lister-item-content'}):
        title = movie.find('a').contents[0]
        print ()
        print (title)
        description = movie.find_all('p', attrs={'class': 'text-muted'})[-1].get_text()
        description = description.encode('ascii', errors = 'ignore').strip().decode()
        
        image_page = movie.find('h3', attrs={'class':'lister-item-header'}).find('a')['href']
        sleep(10)
        img_req = requests.get('https://www.imdb.com' + image_page)
        bs2 = bs4.BeautifulSoup(img_req.text, features="lxml")
        image = bs2.find('div', attrs={'class':'poster'}).find('img')
        print (image)
        save_dir = image_dir + "/" + title
        urllib.request.urlretrieve(image['src'], save_dir)
        list_df.append([title, description, save_dir])
    df = pd.DataFrame(list_df,columns=['Title','Description', 'Image'])
    df.to_csv(const.movie_dataset, encoding='utf-8', index = False)
    


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
    Classifies the dataset of movies based on the emotion they express, as identified from their summaries.

    """
    
    df= pd.read_csv(const.movie_dataset, encoding='utf-8')
    list_df=[]
    for item in df["Description"]:
        list_df.append(getTextSentiment(item))
    X = pd.DataFrame(list_df)
    kmeans = KMeans(n_clusters=7)
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)
    centers = kmeans.cluster_centers_
    list_emotions=['anger', 'fear', 'sadness','tentative', 'analytical','confident','joy']
    list_pred_emotions=[]
    centers_sorted=sorted(centers,key=lambda l:l[0])
    for value in y_kmeans:
        list_pred_emotions.append(list_emotions[value])
    df["Emotion"]=list_pred_emotions
    df.to_csv(const.clustered_movies, sep=',', encoding='utf-8', index = 0)
    
    
def movies_classify():
    """
    Creates the movie dataset and classifies them, if not already done.
    """
    if not os.path.exists(const.movie_dataset):
        getMovieDescription()
    if not os.path.exists(const.clustered_movies):
        Clustering()


def get_movies(emotion):
    """
    Returns a set of movies for a given emotion.

    Args:

    emotion: The emotion for which you want movies to be fetched.

    Returns:

    The set of movies for the particular emotion
    """
    df = pd.read_csv(const.clustered_movies)

    df = df.loc[df['Emotion'] == emotion]
    print (len(df))
    return df.sample(const.movie_num)
    
