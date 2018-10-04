
# coding: utf-8

import pandas as pd
import numpy as np
import os
import copy
import re
import urllib.request
import json
import sklearn.metrics
from constants import Constants
from textblob import TextBlob
from sklearn.metrics import silhouette_score

const = Constants()  


class Classification:
    def __init__(self):

        self.const = Constants()
        self.input_path = self.const.song_dataset
        self.feature_path = self.const.feature_path
        self.output_path =self.const.clustered_music
        self.api_key = self.const.musixmatch_api_key
        self.features = None
        self.details = None
        self.valence = []
        self.arousal = []
        self.clusters = []
    
    def read_details(self):
        """
        Reads the details of all songs in the dataset
        """
        self.details = pd.read_csv(self.input_path)


    def get_lyrics_valence(self, song):
        """
        Gets the lyrics of the song passed as parameter from musixmatch and finds the sentiment polarity

        Args:

        song: a string containing the name of the song

        Returns:

        The polarity of sentiment if the lyrics were foound and -1 if the lyrics weren't found
        """
        print (song)
        print()
        query = urllib.parse.quote(song)
        url="http://api.musixmatch.com/ws/1.1/matcher.lyrics.get?q_track={}&apikey={}".format(query,self.api_key)

        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        response = urllib.request.urlopen(req).read()
        data=json.loads(response)
        if(data["message"]["header"]["status_code"]==200):
       
            lyrics=data["message"]["body"]["lyrics"]["lyrics_body"]
            test= TextBlob(lyrics)
            x=test.sentiment.polarity
            return ((x+1)/2)
        else:
            return -1
    
    def calculate_arousal(self):
        """
        Computes arousal values for all songs in the dataset
        """
        print ('Calculating arousal...')
        for x in self.details.Tempo:
            self.arousal.append(x/270.0)
    
    def calculate_valence(self):
        """
        Computes valence values for all songs in the dataset
        """
        print ('Calculating valence...')
        for x,y,z in zip(self.details.Key, self.details.Mode, self.details.Name):
            x = ((x-5) if x>4 else (x+7))/12
            y = 0.25 if y==0 else 0.75
            
            z=re.sub("[\(\[].*?[\)\]]", "", z)
            p=self.get_lyrics_valence(z)
            self.valence.append((x+y+p)/3)

    def assignment(self, df, centroids):
        """
        Assigns the new 'closest' values based on which new cluster centroid is closest

        Args:

        df: datafrtame containing arousal, valence and closest cluster values for all songs
        centroids: a list containing the co-ordinates of centre points for all clusters

        Returns:

        The modified dataframe containing new 'closest' values
        """
        
        for i in centroids.keys():
            df['distance_from_{}'.format(i)] = (
                np.sqrt(
                    (df['Valence'] - centroids[i][0]) ** 2
                    + (df['Arousal'] - centroids[i][1]) ** 2
                )
            )
        centroid_distance_cols = ['distance_from_{}'.format(i) for i in self.const.music_cluster_centroids.keys()]
        df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
        df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
        return df


    def update(self, df, centroids):
        """
        Calculates the new centroid values for each cluster

        Args:

        df: datafrtame containing arousal, valence and closest cluster values for all songs
        centroids: a list containing the co-ordinates of centre points for all clusters 

        Returns:

        Updated list of co-ordinates of centre points for all clusters     
        """
        for i in centroids.keys():
            centroids[i][0] = np.mean(df[df['closest'] == i]['Valence'])
            centroids[i][1] = np.mean(df[df['closest'] == i]['Arousal'])
        return centroids

    def cluster_songs(self):
        """
        Classifies all songs in the dataset based on emotion
        """
        print ('Clustering songs...')
        df = self.features[['Valence', 'Arousal']].copy()
        df = self.assignment(df, self.const.music_cluster_centroids)
        old_centroids = centroids = copy.deepcopy(self.const.music_cluster_centroids)
        centroids = self.update(df, centroids)

        for i in old_centroids.keys():
            old_x = old_centroids[i][0]
            old_y = old_centroids[i][1]
            dx = (centroids[i][0] - old_centroids[i][0]) * 0.75
            dy = (centroids[i][1] - old_centroids[i][1]) * 0.75

        df = self.assignment(df, centroids)

        while True:
            closest_centroids = df['closest'].copy(deep=True)
            centroids = self.update(df, centroids)
            df = self.assignment(df, centroids)
            if closest_centroids.equals(df['closest']):
                break            

        belongs_to= []

        for a in df['closest']:
            belongs_to.append(a)

        print (belongs_to)
        return belongs_to

        
        
    def write_features(self):
        """
        Writes the calculated features(arousal and valence) to a CSV file
        """
        print ('Writing features...')
        self.features = pd.DataFrame({'ID':self.details.ID, 'Arousal':self.arousal, 'Valence':self.valence})
        self.features.to_csv(self.feature_path, index = False)
              
    def write_clusters(self):
        """
        Writes the details of the clustered music to a CSV file
        """
        clustered_data = pd.DataFrame({'ID':self.details.ID.tolist(), 'Name':self.details.Name.tolist(), 'Artist':self.details.Artist.tolist(), 'Album':self.details.Album.tolist(), 'Year':self.details.Year.tolist(), 'Emotion':[self.const.music_cluster_mappings[x] for x in self.clusters]})
        print (len(clustered_data))
        clustered_data.to_csv(self.output_path, index = False)
        
    def driver_function(self):
        """
        Driver function for the Classification class
        """
        if not os.path.exists(self.feature_path):
            print ('Classifying music...')
            self.read_details()
            self.calculate_arousal()
            self.calculate_valence()
            self.write_features()
        else:
            self.read_details()
            self.features = pd.read_csv(self.feature_path, index_col = 0)
            
        if not os.path.exists(self.output_path):
            self.clusters = self.cluster_songs()
            self.write_clusters()




def music_classify():
    """
    Classifies the music dataset
    """
    classification = Classification()
    classification.driver_function()

def get_songs(emotion):
    """
    Retrieves a set of songs that correspond to a particular emotion

    Args:

    emotion: the emotion of music needed

    Returns:

    A dataframe with details of music that matches the emotion
    """
    df = pd.read_csv(const.clustered_music)
    df = df.loc[df['Emotion'] == emotion]
    return df.sample(const.music_num)

