
# coding: utf-8

import pandas as pd
import numpy as np
import h5py
import os
import glob
import copy
import hdf5_getters
import re
import urllib.request
import json
import sklearn.metrics
import matplotlib.pyplot as plt
from constants import Constants
from textblob import TextBlob
from sklearn.metrics import silhouette_score

const = Constants()
class song_data:
    def __init__(self):
        self.id = []
        self.songCount = 0
        self.title = []
        self.artist = []
        self.album = []
        self.year = []
        self.tempo = []
        self.energy = []
        self.key = []
        self.pitch = []
        self.mfcc = []
        self.mode = []
        self.song_details = None
        self.const = Constants()
        self.file_path = self.const.song_dataset
        self.output_path = self.const.song_details
        
    def update(self, songH5File):
        """
        Updates details for a particular song, and adds them to the existing list
        Args:

        songH5File: the hdf5 file for a song
        """
        
        if '\\x' in str(hdf5_getters.get_title(songH5File))[2:-1]:
            return
        self.id.append(str(hdf5_getters.get_song_id(songH5File))[2:-1])
        self.songCount += 1
        self.title.append(str(hdf5_getters.get_title(songH5File))[2:-1])
        self.artist.append(str(hdf5_getters.get_artist_name(songH5File))[2:-1])
        self.album.append(str(hdf5_getters.get_release(songH5File))[2:-1])
        self.year.append(str(hdf5_getters.get_year(songH5File)))
        self.tempo.append(str(hdf5_getters.get_tempo(songH5File)))
        self.energy.append(str(hdf5_getters.get_energy(songH5File)))
        self.key.append(str(hdf5_getters.get_key(songH5File)))
        self.pitch.append(hdf5_getters.get_segments_pitches(songH5File).mean(axis = 0).argmax(axis = 0))
        self.mfcc.append(hdf5_getters.get_segments_timbre(songH5File).mean(axis = 0).argmax(axis = 0))
        self.mode.append(hdf5_getters.get_mode(songH5File))
        

    def set_paths(self):
        """
        Stores the paths to music information files
        """
        print ('Setting paths...')
        # If file does not exits, create it
        if not os.path.exists(self.const.song_list_path):

            # List all paths of songs and save them to 
            get_song_paths = glob.glob(self.const.song_dataset)
            with open(self.const.song_list_path,'w') as f:
                f.writelines('\n'.join(p for p in get_song_paths))
                f.close()


    def load_data(self):
        """
        loads and updates details of all songs in the dataset
        """
        print ('Loading dataset...')
        get_song_paths = glob.glob(self.const.song_dataset)
        for f in get_song_paths[:1000]:
                songH5File = hdf5_getters.open_h5_file_read(f)
                self.update(songH5File)
                songH5File.close()
        print ('No. of songs : ', len(self.id))
    
    def write_csv(self):
        """
        writes the processed details to a CSV file
        """
        print ('Writing to CSV...')
        self.song_details = pd.DataFrame({'ID':self.id, 'Name':self.title, 'Artist':self.artist, 'Album':self.album, 'Year':self.year, 'Tempo':self.tempo, 'Energy':self.energy, 'Key':self.key, 'Pitch':self.pitch, 'MFCC':self.mfcc, 'Mode':self.mode})
        self.song_details.to_csv(self.output_path, index = False)    
            
            
    def driver_function(self):
        """
        driver function for the song_data class
        """
        if not os.path.exists(self.output_path):
            print ('Extracting song details...')
            self.set_paths()
            self.load_data()
            self.write_csv()
            print ('Written to CSV.')

    


class Classification:
    def __init__(self):

        self.const = Constants()
        self.songs_data = song_data()
        self.input_path = self.const.song_details
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
    song = song_data()
    classification = Classification()
    song.driver_function()
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

