import os
from src import app
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_required
from src import db
from src.main.forms import MovieForm
from src.database.models import Watchlist
from src.main import main
from ml.trained_model import get_suggestions
from get_info import get_info, get_random, get_request
from get_info import get_movie_object, get_movie_info


@main.route('/')
@main.route('/home')
@main.route('/index')
def home():
    return render_template('home.html', title=('Home'))

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='../static/img/favicon.ico')


@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    form = MovieForm()
    if form.validate_on_submit():
        title = form.movie_name.data
        if not get_request(title):
            flash('Movie is not in our database, please check correction of the title!', category='alert-danger')
            return redirect(url_for('.search'))
        title = form.movie_name.data
        return redirect(url_for('.result', page_state='movie', title=title))
    suggestions = get_suggestions()
    return render_template('search.html', suggestions=suggestions, form=form)


@main.route("/random", methods=['GET', "POST"])
@login_required
def randomfilm():
    if request.method == "POST":
        return redirect(url_for('.result', page_state='random'))
    return render_template('random.html')

@main.route('/<page_state>/result', methods=['GET', 'POST'])
@login_required
def result(page_state):
    title = request.args.get('title')
    if not title:
        for i in range(0, 10):
            try:
                title, poster, popularity, genres, overview, vote_average, vote_count, release_date, runtime, \
                status, movie_id, casts, cast_details, movie_reviews, movie_cards = get_info(*get_random())
            except Exception:
                print("Error")
            else:
                break
    else:
        title, poster, popularity, genres, overview, vote_average, vote_count, release_date, runtime, \
        status, movie_id, casts, cast_details, movie_reviews, movie_cards = get_info(*get_request(title))
    return render_template('result.html', title=title, overview=overview, poster=poster,
                           popularity=popularity, vote_average=vote_average, vote_count=vote_count,
                           release_date=release_date, runtime=runtime, status=status, genres=genres,
                           movie_cards=movie_cards, movie_id=movie_id,
                           reviews=movie_reviews, casts=casts, cast_details=cast_details, page_state=page_state)



# watchlist
@main.route("/watchlist", methods=["GET"])
@login_required
def watchlist():
    try:
        user_id = int(current_user.get_id())
        films = Watchlist.query.filter_by(user_id=user_id).all()
        films = [get_movie_info(get_movie_object(film.movie_id)) for film in films]
        movie_cards = [(x[0], x[1], round(x[2], 1), x[3], round(x[5], 1), x[10]) for x in films]
        return render_template('watchlist.html', movie_cards=movie_cards)
    except:
        return "", 404



@main.route('/movie/<int:id>', methods=["DELETE"])
@login_required
def delete(movie_id=None):
    try:
        Watchlist.query.filter_by(movie_id=movie_id).delete()
        db.session.commit()
    except:
        return "", 404
    return "", 200


@main.route('/movie/<int:movie_id>', methods=["GET"])
@login_required
def post(movie_id=None):
    # if current_user.is_authenticated():
    user_id = int(current_user.get_id())
    try:
        watch_list = Watchlist(movie_id=movie_id, user_id=user_id)
        db.session.add(watch_list)
        db.session.commit()
    except:
        return {"message": "This film is already added!"}, 409
    return "", 200