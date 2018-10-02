# MoodSeek

MoodSeek is a web application developed in Python using Flask that helps identify the user’s mood based on their social media activity, and suggests music, books, movies, quotes and images that might appeal to the user.

For further details about the application, please read idea_doc.docx and watch MoodSeek.mp4 for a demonstration of the working system.

## Documentation

This project is an entry to the #IBMHackChallenge and the relevant documentation is outlined below:

* __I-idea_doc__ : 

## How to run the system :

* Install dependencies : Python 3.5, Flask, IBM Watson API, tweepy, nltk, scikit, BeautifulSoup4, urllib, textblob, h5py, glob in addition to other commonly used packages.

* Download the Million Song Subset from http://static.echonest.com/millionsongsubset_full.tar.gz and extract it into data/music.

* Run __ui_driver.py__.


## The files in this repository : 

* __books.py__ : Creates a dataset of books by scraping GoodReads, clusters and retrieves books that matches the user’s emotion.
* __constants.py__ : Specifies constant values that are used by all other files in the system.
* __hdf5_getters.py__ - Setup functions to access fields from the Million Songs Dataset. This is part of the Million Song Dataset project from LabROSA, obtained from https://github.com/tbertinmahieux/MSongsDB/blob/master/PythonSrc/hdf5_getters.py
* __images.py__ :  Retrieves images that matches the user’s emotion
* __movies.py__ : Creates a dataset of movies by scraping IMDB, clusters, and retrieves movie that matches the user’s emotion.
* __quotes.py__ : Creates a dataset of movies by scraping quotes, and retrieves movie that matches the user’s emotion.
* __recommendations.py__ : Retrieves recommendation based on the user’s emotion, and also drives recommendations for all forms of entertainment.
* __twitter.py__ : Scrapes twitter data based on handle for a fixed time period, and identifies user’s emotions from the tweet data. It also allows for emotion recognition from an essay written by the user.
* __ui_driver.py__ : The flask app that drives the entire system.
