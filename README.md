# MoodSeek

MoodSeek is a web application developed in Python using Flask that helps identify the user’s mood based on their social media activity, and suggests music, books, movies, quotes and images that might appeal to the user.

For a more detailed explanation, please refer the documentation described below.


## Documentation

This project is an entry to the #IBMHackChallenge and the relevant documentation (present in the documentation folder) is outlined below:

* __I-MoodSeek-ideation_doc__ : Describes the problem statement, team member roles and the scope of work carried out.

* __II-MoodSeek-presentation__ : A short presentation on the entry.

* __III-MoodSeek-video_recording__ : A demonstration of the working of the app, followed by USPs and the design process of the system.

      Timestamps : 
  
         0:00 - Introduction
         
         0:35 - Demonstration

         4:48 - Key Value Propositions and USPs

         8:19 - Design of the system

* __IV-MoodSeek-key_value_proposition__ : Key Value Proposition/innovations being proposed and developed on top of the given problem statement that create uniqueness in the solution.


## How to run the system

* Run __install_dependencies.py__ to install all required dependencies.

* Run __ui_driver.py__ to run the app.


## Files in this repository

* __books.py__ : Creates a dataset of books by scraping GoodReads, clusters and retrieves books that matches the user’s mood.
* __constants.py__ : Defines constant values that are used by all other files in the system.
* __images.py__ :  Retrieves images that matches the user’s emotion
* __install_dependencies.py__ : Installs python packages required to run the app.
* __movies.py__ : Creates a dataset of movies by scraping IMDB, clusters, and retrieves movie that matches the user’s mood.
* __music.py__ : Analyses and classifies a music dataset, and retrieves music that matches the user's mood.
* __quotes.py__ : Creates a dataset of movies by scraping quotes, and retrieves movie that matches the user’s mood.
* __recommendations.py__ : Retrieves recommendation based on the user’s emotion, and also drives recommendations for all forms of entertainment.
* __twitter.py__ : Scrapes twitter data based on handle for a fixed time period, and identifies user’s emotions from the tweet data. It also allows for emotion recognition from an essay written by the user.
* __ui_driver.py__ : The flask app that drives the entire system.


## Notes

The music dataset was derived from the Million Song Dataset (https://labrosa.ee.columbia.edu/millionsong/).

The twitter extraction module was derived from https://github.com/alexmille/twitter-data-extractor.

All image credits to the rightful owners.


