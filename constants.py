class Constants:
        def __init__(self):
                self.user_emotions = ['joy', 'fear', 'sadness', 'anger', 'analytical', 'confident', 'tentative']
                self.emotion_dict = {'positive':['joy', 'analytical', 'confident'], 'negative':['fear', 'sadness', 'anger', 'tentative']}
                self.emotion_verb = {'joy':'happy', 'fear':'scared', 'sadness':'sad', 'anger':'angry', 'analytical':'analytical', 'confident':'confident', 'tentative':'tentative'}
                self.recs_path = 'data/recommendations.pickle'
                self.song_key = 'songs'
                self.movie_key = 'movies'
                self.book_key = 'books'
                self.image_key = 'images'
                self.quote_key = 'quotes'
                
                #Twitter API credentials
                self.twitter_consumer_key = "your_consumer_key"
                self.twitter_consumer_secret = "your_consumer_secret"
                self.twitter_access_key = "your_access_key"
                self.twitter_access_secret = "your_access_secret"
                #Musixmatch
                self.musixmatch_api_key = "your_api_key"
                #IBM Watson
                self.watson_username = 'your_watson_username'
                self.watson_password = 'your_watson_password'


                self.tweets_raw = 'data/twitter/%s_tweets.csv'
                self.tweets_json = 'data/twitter/tweets.json'

                
                self.song_dataset = 'data/music/songDetails.csv'
                self.feature_path = 'data/music/features.csv'
                self.clustered_music = 'data/music/clustered_music.csv'
                self.music_emotion_mapping = {'soothe':{'joy':'happy', 'fear':'hopeful', 'sadness':'hopeful', 'anger':'contemplative', 'analytical':'contemplative', 'confident':'happy', 'tentative':'happy'}, 'relatable':{'joy':'happy', 'fear':'afraid', 'sadness':'sad', 'anger':'angry', 'analytical':'contemplative', 'confident':'happy', 'tentative':'discontent'}}
                self.music_cluster_mappings = { 1:'happy', 2:'calm', 3:'hopeful', 4:'pleased', 5:'sad', 6:'angry', 7:'discontent', 8:'content', 9:'afraid', 10:'contemplative'}
                self.music_cluster_centroids = {1:[0.945,0.585], 2:[0.89,0.16], 3:[0.805,0.35], 4:[0.945,0.45], 5:[0.095, 0.3], 6:[0.3, 0.895], 7: [0.16, 0.34], 8: [0.905,0.225], 9: [0.44, 0.895] ,10: [0.79, 0.2]}
                self.music_num = 13

                self.quotes_url = "https://www.brainyquote.com/topics/"
                self.quotes_emotions_mapping = {'joy':'happiness','fear':'fear','sadness':'sad', 'anger':'anger', 'analytical':'wisdom', 'confident':'motivational', 'tentative':'movingon'}
                self.clustered_quotes = 'data/quotes/clustered_quotes.csv'

                
                self.movies_url = 'https://www.imdb.com/search/title?sort=num_votes,desc&start=1&title_type=feature&year=1950,2012'
                self.movie_dataset = 'data/movies/movie_imdb.csv'
                self.clustered_movies = 'data/movies/movie_imdb_clustering.csv'
                self.movies_image_dir = 'static/data/movies'
                self.movie_emotion_mapping = {'relatable':{'joy':'joy', 'fear':'fear', 'anger':'anger', 'sadness':'sadness', 'confident':'confident', 'analytical':'analytical', 'tentative':'tentative'}, 'soothe':{'joy':'joy', 'fear':'joy', 'anger':'joy', 'sadness':'joy', 'confident':'confident', 'analytical':'analytical', 'tentative':'confident'}}
                self.movie_num = 4

                self.image_dataset = './static/data/images'
                self.image_emotion_mapping = {'relatable':{'joy':'joy', 'fear':'neutral', 'anger':'neutral', 'sadness':'neutral', 'confident':'joy', 'analytical':'analytical', 'tentative':'neutral'}, 'soothe':{'joy':'joy', 'fear':'joy', 'anger':'joy', 'sadness':'joy', 'confident':'joy', 'analytical':'analytical', 'tentative':'neutral'}}
                self.clustered_images = 'data/images/Images_emotion.csv'
                self.images_dir = 'static/data/images'
                self.image_num = 10

                self.book_url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever'
                self.book_dataset = 'data/books/books_goodreads.csv'
                self.clustered_books = 'data/books/books_goodreads_clustering.csv'
                self.books_image_dir = 'static/data/books'
                self.book_emotion_mapping = {'relatable':{'joy':'joy', 'fear':'fear', 'anger':'anger', 'sadness':'sadness', 'confident':'confident', 'analytical':'analytical', 'tentative':'tentative'}, 'soothe':{'joy':'joy', 'fear':'joy', 'anger':'joy', 'sadness':'joy', 'confident':'confident', 'analytical':'analytical', 'tentative':'confident'}}
                self.book_num = 4
