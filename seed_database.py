""" Script and Seed Movie Ratings Database """

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

# load data from json file and creates Movie objects for database
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (movie['title'], 
                                  movie['overview'], 
                                  movie['poster_path'])

    release_date = datetime.strptime(movie['release_date'],"%Y-%m-%d")
    new_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(new_movie)


# creates random users for database
for n in range(10):
    email = f'user{n}@test.com'  # a unique email :)
    password = 'test'

    # create a user, a score, and choose a movie
    new_user = crud.create_user(email, password)

    # make a new rating for the database
    for n in range(10):
        score = randint(1, 5)
        movie = choice(movies_in_db)
        
        new_rating = crud.create_rating(user=new_user, movie=movie, score=score)