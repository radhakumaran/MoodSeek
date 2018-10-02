#MoodSeek

MoodSeek is a web application developed in Python using Flask that helps identify the user’s mood based on their social media activity, and suggests music, books, movies, quotes and images that might appeal to the user.

For further details about the application, please read idea_doc.docx and watch MoodSeek.mp4 for a demonstration of the working system.


##How to run the system :

Install dependencies - Python 3.5, Flask, IBM Watson API, tweepy, nltk, scikit, BeautifulSoup4, urllib, textblob, h5py, glob in addition to other commonly used packages.

##The files in this repository : 

Books.py - Creates a dataset of books by scraping GoodReads, clusters and retrieves books that matches the user’s emotion.
Constants.py - Specifies constant values that are used by all other files in the system.
Hdf5_getters.py - Setup functions to access fields from the Million Songs Dataset. This is part of the Million Song Dataset project from LabROSA
Images.py -  Retrieves images that matches the user’s emotion
Movies.py - Creates a dataset of movies by scraping IMDB, clusters, and retrieves movie that matches the user’s emotion.
Quotes.py - Creates a dataset of movies by scraping quotes, and retrieves movie that matches the user’s emotion.
Recommendations.py - Retrieves recommendation based on the user’s emotion, and also drives recommendations for all forms of entertainment.
Twitter.py - Scrapes twitter data based on handle for a fixed time period, and identifies user’s emotions from the tweet data. It also allows for emotion recognition from an essay written by the user.
Ui_driver.py - The flask app that drives the entire system.

