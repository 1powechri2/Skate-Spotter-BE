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
def get_spots():
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


@app.route('/api/v1/spots/<int:id>')
def get_spot(id=1):
    skater_spot = session.query(SkateSpot).get(id)

    if skater_spot != None:
        spot = {'id': skater_spot.id, 'name': skater_spot.name,
        'description': skater_spot.description,
        'street_name': skater_spot.street_name,
        'latitude': skater_spot.latitude,
        'longitude': skater_spot.longitude,
        'skater_id': skater_spot.skater_id,
        'photos': [{'url': photo.url} for photo in skater_spot.photos],
        'rating': [favorite.rating for favorite in skater_spot.favorites].count(True)/
        len([favorite.rating for favorite in skater_spot.favorites]),
        'number_of_ratings': len([favorite.rating for favorite in skater_spot.favorites])}
    else:
        spot = {'404': f'There is nothing in the database with an id of {id}.'}

    return jsonify(spot)

@app.route('/api/v1/skaters')
def get_skaters():
    skaters = session.query(Skater).all()

    dudes = [{'id': skater.id, 'name': skater.name,
    'tag': skater.tag,

    'skate_spots': [{'id': spot.id, 'name': spot.name,
    'description': spot.description,
    'street_name': spot.street_name,
    'latitude': spot.latitude,
    'longitude': spot.longitude,
    'skater_id': spot.skater_id,
    'photos': [{'url': photo.url} for photo in spot.photos],
    'rating': [favorite.rating for favorite in spot.favorites].count(True)/
    len([favorite.rating for favorite in spot.favorites]),
    'number_of_ratings': len([favorite.rating for favorite in spot.favorites])}
    for spot in skater.spots]}
    for skater in skaters]

    return jsonify(dudes)

@app.route('/api/v1/skaters/<int:id>')
def get_skater(id=1):
    skater = session.query(Skater).get(id)

    if skater != None:
        dude = {'id': skater.id, 'name': skater.name,
        'tag': skater.tag,
        'skate_spots': [{'id': spot.id, 'name': spot.name,
        'description': spot.description,
        'street_name': spot.street_name,
        'latitude': spot.latitude,
        'longitude': spot.longitude,
        'skater_id': spot.skater_id,
        'photos': [{'url': photo.url} for photo in spot.photos],
        'rating': [favorite.rating for favorite in spot.favorites].count(True)/
        len([favorite.rating for favorite in spot.favorites]),
        'number_of_ratings': len([favorite.rating for favorite in spot.favorites])}
        for spot in skater.spots]}
    else:
        dude = {'404': f'There is nothing in the database with an id of {id}.'}

    return jsonify(dude)

if __name__ == '__main__':
    app.run(debug=True)
