from flask import Flask, render_template, request, json, session, url_for, redirect, flash
app = Flask(__name__)


import pickle
import re
from constants import Constants
from recommendations import Recommendations
from twitter import get_twitter_emotion, get_essay_emotion, get_name




const = Constants()



class Data:
    def __init__(self):
        self.twitter_handle = ''
        self.name = ''
        self.emotion = ''
        self.essay = False
        self.essay_path = ''
        self.songs = None
        self.books = None
        self.movies = None
        self.images = None
        self.quotes = None
        self.choice = None
        self.screen = 0
        self.rec = Recommendations()


    def set_twitter_handle(self, twitter_handle):
        self.twitter_handle = twitter_handle

    def get_twitter_handle(self):
        return self.twitter_handle

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_essay(self, essay):
        self.essay = essay

    def get_essay(self):
        return self.essay

    def set_essay_path(self, path):
        self.essay_path = path

    def get_essay_path(self):
        return self.essay_path

    def set_emotion(self, emotion):
        self.emotion = emotion

    def get_emotion(self):
        return self.emotion

    def set_songs(self, songs):
        self.songs = songs

    def get_songs(self):
        return self.songs

    def set_books(self, books):
        self.books = books

    def get_books(self):
        return self.books

    def set_movies(self, movies):
        self.movies = movies

    def get_movies(self):
        return self.movies

    def set_images(self, images):
        self.images = images

    def get_images(self):
        return self.images

    def set_quotes(self, quotes):
        self.quotes = quotes

    def get_quotes(self):
        return self.quotes

    def set_choice(self, choice):
        self.choice = choice

    def get_choice(self):
        return self.choice

    def find_emotion(self):
        """
        Identifies and sets the user's name and mood(emotion)
        """

        if self.essay == False:
            self.set_name(get_name(self.twitter_handle))
            self.set_emotion(get_twitter_emotion(self.twitter_handle))
        else:
            self.set_emotion(get_essay_emotion(self.essay_path))
        
        print ('Your name :', self.get_name())
        print ('Your mood :', self.get_emotion())

    def initialise_recommendations(self):
        """
        Classifies the datasets if necessary
        """
        
        self.rec.initialise_recommendations()
        
    
    def get_recommendations(self):
        """
        Gets recommendations for the user based on their mood
        """
        
        self.rec.get_recommendations(self.get_emotion(), self.get_choice())
        
        with open(const.recs_path, 'rb') as handle:
            recs = pickle.load(handle)
        self.songs = recs[const.song_key]
        self.movies = recs[const.movie_key]
        self.books = recs[const.book_key]
        self.images = recs[const.image_key]
        self.quotes = recs[const.quote_key]

    def clear(self):
        """
        Clears user data
        """
        self.twitter_handle = ''
        self.name = ''
        self.emotion = ''
        self.essay = False
        self.songs = None
        self.books = None
        self.movies = None
        self.images = None
        self.quotes = None
        self.choice = None
        self.rec = Recommendations()
        
        
     
        


data = Data()


@app.route("/results", methods = ['POST', 'GET'])
def results():
    """
    Displays the user's results
    """    
    print ('Getting results...')
    print (data.get_choice())
    data.get_recommendations()

    new_songs=[]

    for key, value in data.get_songs().iterrows():
        #print("Hiiiiii {}".format(value['Name'])
        sng=value['Name'].lower() + " " + value['Artist'].lower()
        sng=re.sub("[\(\[].*?[\)\]]", "", sng)
        sng=sng.replace(" ","%20")
        link="https://soundcloud.com/search?q={}&query_urn=soundcloud%3Asearch-autocomplete%3Ab55a0bd13ccb4ff8962d38cf41d38885".format(sng)
        print(value['Name'])

        new_songs.append([key, value, link])
    
    return render_template('results.html', name = data.get_name(), emotion = const.emotion_verb[data.get_emotion()], songs = new_songs, movies = data.get_movies(), books = data.get_books(), images = data.get_images(), quote = data.get_quotes())
    

@app.route("/choice", methods = ['POST', 'GET'])
def choice():
    """
    Asks user whether they want soothing recommendations or relatable recommendations
    """
    if data.get_emotion() in const.emotion_dict['positive']:
        data.set_choice(1)
        return redirect(url_for('results'))
    
    print ('Emotion : ', data.emotion)
    print ('Evaluating results...')
    
    if request.method == 'POST':
        print ('Posted.')
        choice = int(request.form['choice'])
        data.set_choice(choice)
        print (choice)
        print ('Going to results page.')
        return redirect(url_for('results'))

    
    return render_template('choice.html', name = data.get_name(), emotion = const.emotion_verb[data.get_emotion()])

   

@app.route("/get-handle", methods = ['POST', 'GET'])
def get_handle():
    """
    Gets the user's twitter handle
    """
    data.clear()
    if request.method == 'POST' :
        if 'twitter' in request.form:
            twitter_handle = str(request.form['twitter'])
            data.set_twitter_handle(twitter_handle)
            data.set_name(twitter_handle)
            print (twitter_handle)
            data.find_emotion()
            return redirect(url_for('choice'))
    return render_template("twitter.html")


@app.route("/essay", methods = ['POST', 'GET'])
def essay():
    print ('2')
    if request.method == 'POST':
        print (request.form)
        if 'essay' in request.form:
            data.set_essay(True)
            data.set_name(str(request.form['name']))
            data.set_essay_path(str(request.form['essay']))
            data.find_emotion()
            return redirect(url_for('choice'))
    return render_template("essay.html")

@app.route("/", methods = ["POST", "GET"])
def index():
        data.rec.initialise_recommendations()
        return redirect(url_for("get_handle"))

if __name__ == '__main__':
        app.run(debug = True)
        
