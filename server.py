"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """ View homepage """
    return render_template('homepage.html')

@app.route('/movies')
def view_all_movies():
    """ View a list of all movie titles """

    all_movies = crud.return_all_movies()

    return render_template('all_movies.html', all_movies=all_movies)

@app.route('/movies/<movie_id>')
def show_movie_detail(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)
    print(movie)

    return render_template('movie_details.html', movie=movie)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
