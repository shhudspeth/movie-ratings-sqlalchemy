"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# session = "eyJjYXJ0IjpbMiwyLDE0LDIsMiwyLDJdfQ.CP0ryA2EMSZdE"

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

    movie_d = crud.get_movie_by_id(movie_id)
    
    
    return render_template('movie_details.html', movie=movie_d)

@app.route('/movies/<movie_id>', methods=["POST"])
def make_movie_rating(movie_id):
    """Update a movie page with a user rating; store new rating in database."""

    movie_d = crud.get_movie_by_id(movie_id)
    user_d = crud.get_user_by_id(session['user']['id'])
    score = request.form['score']
    print("VARIABLES TO USE", score, user_d, movie_d)
    
    new_rating = crud.create_rating(user_d, movie_d, score)
    
    session['rating'] = {movie_d.movie_id:score}
    print(session['rating'])
    flash(f"You made a rating! {new_rating.score}")

    return redirect('/')


@app.route('/users')
def view_all_users():
    """ View a list of all user"""
    all_users = crud.return_all_users()

    return render_template('all_users.html', all_users=all_users)

@app.route('/users', methods=["POST"])
def register_new_user():
    """ Checks for and or registers a new user"""
    email = request.form['email']
    user = crud.get_user_by_email(email)
    session['show_login'] = True
    session['show_form'] = True
    session['rating']=[]

    if user:
        flash("User, you already have an account. Please login")
        session['show_form'] = False
        session['show_login'] = True
        return redirect('/')

    else:
        flash('creating new user')
        password = request.form['password']
        crud.create_user(email, password)

    return redirect('/')

@app.route('/login', methods=["POST"])
def login_user():
    """ Checks for and or registers a new user"""
    # get email and password from html form post
    email = request.form['email']
    password = request.form['password']

    # get user info from db using crud function
    user = crud.get_user_by_email(email)
    session['show_form'] = False
        

    # check to see if password in db matches form password 
    if user.password==password:
        session['user'] = {'id': user.user_id, 'email': user.email}
        session['show_form'] = False
        session['show_login'] = False
        flash("User, you are logged in!")
        return redirect('/')

    else:
        flash('Incorrect password or email. Please try again')   
        return redirect('/')


@app.route('/users/<user_id>')
def show_user_detail(user_id):
    """Show details on a user."""

    user_d = crud.get_user_by_id(user_id)
    
    return render_template('user_details.html', user=user_d)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
