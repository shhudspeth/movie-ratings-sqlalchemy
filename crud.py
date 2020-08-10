""" CRUD OPERATIONS"""

from model import db, User, Movie, Rating, connect_to_db



# Functions start here!
def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def return_all_users():
    """ Create and return a list of all users"""
    return User.query.all()  


def get_user_by_id(user_id):
    """Return a user by id"""
    return User.query.get(user_id)

def get_user_by_email(user_email):
    """ Return a user by email"""
    
    return User.query.filter(User.email==user_email).first()


def create_movie(title, overview, release_date, poster_path):
    """ Create and return a new movie"""
    movie = Movie(title=title, 
                  overview=overview, 
                  release_date=release_date, 
                  poster_path=poster_path)
    
    db.session.add(movie)
    db.session.commit()

    return movie


def return_all_movies():
    """ Create and return a list of all movies"""
    return Movie.query.all()  


def get_movie_by_id(movie_id):
    """Return a movie by id"""
    return Movie.query.get(movie_id)


def create_rating(user, movie, score):
    """ Create and return a new rating with movie and user information"""
    rating = Rating(user=user, movie=movie, 
                    score=score)
    
    db.session.add(rating)
    db.session.commit()

    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)