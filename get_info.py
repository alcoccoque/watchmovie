import re
import urllib
import bs4 as bs
import numpy as np
import pandas as pd
from src.ml.trained_model import load
import tmdbv3api as tmdb3

tmdb = tmdb3.TMDb()
tmdb.api_key = 'df67c6cc529840b0a18cd7017e1f2fd1'
movie = tmdb3.Movie()
person = tmdb3.Person()
filename, clf, vectorizer = load()

genres = {28: "Action",
          12: "Adventure", 16: "Animation",
          35: "Comedy", 80: "Crime",
          99: "Documentary", 18: "Drama",
          10751: "Family", 14: "Fantasy",
          36: "History", 27: "Horror",
          10402: "Music", 9648: "Mystery",
          10749: "Romance", 878: "Science Fiction",
          10770: "TV Movie", 53: "Thriller",
          10752: "War", 37: "Western"}


def get_cast_info(c: object) -> tuple:
    """
    get info about recommended films
    :param c: details cast object
    :return: tuple of details about cast
    """
    print("\n\n CAST IFO START \n\n")
    cast_ids = list(map(lambda x: x['id'], c))
    p = [person.details(i) for i in cast_ids]
    cast_names = list(map(lambda x: x['name'], c))
    cast_chars = list(map(lambda x: x['character'], c))
    cast_bdays = list(map(lambda x: x.birthday, p))
    cast_bios = list(map(lambda x: x.biography, p))
    cast_places = list(map(lambda x: x.place_of_birth, p))
    cast_profiles = list(
        map(lambda x: 'https://image.tmdb.org/t/p/original' + str(x.profile_path) if x.profile_path else
        '../static/img/person-actor.jpg',
            p))
    for i in range(len(cast_bios)):
        cast_bios[i] = cast_bios[i].replace(r'\n', '\n').replace(r'\"', '\"')

    # combining multiple lists as a dictionary which can be passed
    # to the html file so that it can be processed easily and the order of information will be preserved

    casts = {cast_names[i]: [cast_ids[i], cast_chars[i], cast_profiles[i]] for i in range(len(cast_profiles))}

    cast_details = {cast_names[i]: [cast_ids[i], cast_profiles[i], cast_bdays[i], cast_places[i], cast_bios[i]]
                    for
                    i in
                    range(len(cast_places))}
    return casts, cast_details


def get_movie_info(r: object) -> tuple:
    """
    get info about recommended films
    :param r: details tdbm object
    :return: tuple of details about movie
    """
    # movie info
    title = r.title
    poster = 'https://image.tmdb.org/t/p/original' + x if (x := r.poster_path) else '../static/img/poster.jpg'
    popularity = x if (x := r.popularity) else "Unknown"
    genres = [i['name'] for i in r.genres][:3]
    overview = r.overview
    vote_average = x if (x := r.vote_average) else "Unknown"
    vote_count = x if (x := r.vote_count) else "Unknown"
    release_date = x if (x := r.release_date) else "Unknown"
    if (x := r.runtime) % 60 == 0:
        runtime = str(round(x / 60)) + " hour(s)"
    else:
        runtime = str(round(x / 60)) + " hour(s) " + str((x % 60)) + " min(s)"
    status = x if (x := r.status) else "Unknown"
    movie_id = r.id
    return title, poster, popularity, genres, overview, vote_average, \
           vote_count, release_date, runtime, status, movie_id


def get_reviews_info(r: object) -> tuple:
    """
    get info about recommended films
    :param r: details tdbm object
    :return: tuple of details about reviews
    """

    imdb_id = r.imdb_id
    # web scraping to get user reviews from IMDB site
    sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
    soup = bs.BeautifulSoup(sauce, 'html.parser')
    soup_result = soup.find_all("div", {"class": "text show-more__control"})
    reviews_list = []  # list of reviews  
    reviews_status = []  # list of comments (good or bad)
    for reviews in soup_result:
        if reviews.string and len(reviews.string) < 1000:
            reviews_list.append(reviews.string)
            # passing the review to our model
            movie_review_list = np.array([reviews.string])
            movie_vector = vectorizer.transform(movie_review_list)
            pred = clf.predict(movie_vector)
            reviews_status.append('positive' if pred else 'negative')

    # combining reviews and comments into a dictionary
    movie_reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))}
    if movie_reviews:
        return movie_reviews
    else:
        movie_reviews = {"status": "Sorry, there are no comments yet!"}
        return movie_reviews

def get_recommends_info(r: object) -> tuple:
    """
    get info about recommended films
    :param r: details tdbm object
    :return: tuple of details about recommended movies
    """
    rec_films = movie.recommendations(r.id)
    rec_films_title = list(map(lambda x: x.original_title, rec_films))
    rec_films_id = list(map(lambda x: x.id, rec_films))
    rec_films_popularity = list(map(lambda x: round(x.popularity, 1), rec_films))
    rec_films_average = list(map(lambda x: round(x.vote_average, 1), rec_films))
    rec_films_poster_path = ['https://image.tmdb.org/t/p/original' + rec_film.poster_path
                             if rec_film.poster_path else '../static/img/poster.jpg' for rec_film in rec_films]
    genre_ids = [item.genre_ids for item in rec_films]
    rec_films_genres = [list(map(lambda x: genres[int(x)], genre))[:3] for genre in genre_ids]
    movie_cards = zip(rec_films_title, rec_films_poster_path, rec_films_popularity, rec_films_genres,
                      rec_films_average, rec_films_id)
    return movie_cards


def get_movie_object(id: int) -> object:
    """
    get movie details object
    """
    try:
        r = movie.details(id)
        return r
    except Exception:
        print("This movie is not in our database")


def get_request(title: str) -> tuple:
    """
    get movie classes according to movie title
    :param title: movie title
    :return: movie object, cast list
    """
    try:
        res = movie.search(title)[0]
        r = movie.details(res.id)
        c = movie.credits(r.id).cast[:8]
        return r, c
    except Exception:
        print("This movie is not in our database")


def get_random() -> tuple:
    """
    Get random movie classes in range 1-100000
    :return: movie object, cast list
    """
    movies = pd.read_csv("src/datasets/movies.csv", delimiter=',', usecols=['title'])
    try:
        title = movies.sample()['title'].item()
        title = re.sub('[^a-zA-Z]', ' ', title)
        res = movie.search(title)[0]
        r = movie.details(res.id)
        c = k[:8] if len(k := movie.credits(r.id).cast) > 8 else k
        return r, c
    except Exception:
        get_random()


def get_info(r: object, c: list) -> tuple:
    """
    get all info about movie. cast. recommended films
    :param r: details tdbm object
    :param c: cast tdbm list
    :return: tuple of info about film
    """
    try:
        # movie info
        title, poster, popularity, genres, overview, vote_average, \
        vote_count, release_date, runtime, status, movie_id = get_movie_info(r)

        # cast info
        casts, cast_details = get_cast_info(c)

        # reviews
        movie_reviews = get_reviews_info(r)

        # recommended films
        movie_cards = get_recommends_info(r)

        return title, poster, popularity, genres, overview, vote_average, vote_count, release_date, runtime, \
               status, movie_id, casts, cast_details, movie_reviews, movie_cards

    except Exception:
        print("Info about movie isn't full")
