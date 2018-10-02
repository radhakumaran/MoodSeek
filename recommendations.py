import pickle
from constants import Constants
from quotes import fetch_quotes, get_the_quote
from music import music_classify, get_songs
from movies import movies_classify, get_movies
from images import ImageDatasetProcessing, get_images
from books import books_classify, get_books



class Recommendations:
        def __init__(self):
                
                self.const = Constants()
                self.recs_path = self.const.recs_path

        def initialise_recommendations(self):
                """
                
                """
                print ()
                print ('Initialising recommendations...')
                music_classify()
                movies_classify()
                books_classify()
                fetch_quotes()
                ImageDatasetProcessing()
                print ('Initialised recommendations.')
                print ()

        def get_recommendations(self, emotion, choice):
                """
                """
                print ()
                print ('Getting recommendations...')
                rec_dict = {}               
                rec_dict[self.const.quote_key] = get_the_quote(self.const.quotes_emotions_mapping[emotion])
                if choice==1:
                        rec_dict[self.const.song_key] = get_songs(self.const.music_emotion_mapping['relatable'][emotion])
                        rec_dict[self.const.movie_key] = get_movies(self.const.movie_emotion_mapping['relatable'][emotion])
                        rec_dict[self.const.image_key] = get_images(self.const.image_emotion_mapping['relatable'][emotion])
                        rec_dict[self.const.book_key] = get_books(self.const.book_emotion_mapping['relatable'][emotion])
                else:
                        rec_dict[self.const.song_key] = get_songs(self.const.music_emotion_mapping['soothe'][emotion])
                        rec_dict[self.const.movie_key] = get_movies(self.const.movie_emotion_mapping['soothe'][emotion])
                        rec_dict[self.const.image_key] = get_images(self.const.image_emotion_mapping['soothe'][emotion])
                        rec_dict[self.const.book_key] = get_books(self.const.book_emotion_mapping['soothe'][emotion])

                print (rec_dict[self.const.song_key])
                print (rec_dict[self.const.book_key])
                print (rec_dict[self.const.movie_key])
                print (rec_dict[self.const.image_key])
                print (rec_dict[self.const.quote_key])

                with open(self.const.recs_path, 'wb') as handle:
                        pickle.dump(rec_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


