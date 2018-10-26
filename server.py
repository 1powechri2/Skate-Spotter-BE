from flask import Flask, request, render_template
from flask import jsonify
import db_models
from db_models import SkateSpot, Skater, Photo, Favorites
from IPython import embed

app = Flask(__name__)

session = db_models.Session()

@app.route('/')
def hello():
    return 'SKATEBOARDING IS NOT A CRIME'

@app.route('/api/v1/spots')
def spots():
    skater_spots = session.query(SkateSpot).all()

    spots = [{'id': spot.id, 'name': spot.name,
    'description': spot.description,
    'street_name': spot.street_name,
    'latitude': spot.latitude,
    'longitude': spot.longitude,
    'skater_id': spot.skater_id,
    'photos': [{'url': photo.url} for photo in spot.photos],
    'rating': [favorite.rating for favorite in spot.favorites].count(True)/
    len([favorite.rating for favorite in spot.favorites]),
    'number_of_ratings': len([favorite.rating for favorite in spot.favorites])}
    for spot in skater_spots]

    return jsonify(spots)


# @app.route('/user/<int:id>')
# def no_query_string(id=1):
#     return '<h1> The Query id is ' + str(id) + '</h1>'

if __name__ == '__main__':
    app.run(debug=True)
