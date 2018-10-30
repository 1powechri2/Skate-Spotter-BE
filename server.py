from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from db_models import SkateSpot, Skater, Photo, Favorites
from IPython import embed
from werkzeug.security import generate_password_hash, check_password_hash
import db_models
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

term = db_models.Session()

@app.route('/')
def hello():
    return 'SKATEBOARDING IS NOT A CRIME'

@app.route('/api/v1/spots')
def get_spots():
    skater_spots = term.query(SkateSpot).all()

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
    skater_spot = term.query(SkateSpot).get(id)

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

@app.route('/api/v1/skaters', methods=['GET', 'POST'])
def request_skaters():
    if request.method == 'GET':
        skaters = term.query(Skater).all()

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
    elif request.method == 'POST':
        skater_json = json.loads(request.data)

@app.route('/api/v1/skaters/<int:id>')
def get_skater(id=1):
    skater = term.query(Skater).get(id)

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

@app.route('/api/v1/sign_up', methods=['POST'])
def create_skater():
    if 'user_id' in session:
        return jsonify({'Error': 'You are already Signed Up.'})
    else:
        skater_json = json.loads(request.data)
        password = generate_password_hash(skater_json['password'])
        skater = Skater(name=skater_json['name'] , tag=skater_json['tag'],
        email=skater_json['email'], password=password)
        term.add(skater)
        term.commit()

        session['user_id'] = skater.id

        return redirect(url_for('skater_page'))

@app.route('/api/v1/login', methods=['POST'])
def login_skater():
    if 'user_id' in session:
        return jsonify({'Error': 'You are already Logged In.'})
    else:
        skater_json = json.loads(request.data)
        skater = term.query(Skater).filter(Skater.name == skater_json['name'])

        if check_password_hash(skater[0].password, skater_json['password']) == True:
            session['user_id'] = skater[0].id

            return redirect(url_for('skater_page'))
        else:
            {'404': f'There is nothing in the database with an id of {id}.'}

        return jsonify({'Error': 'Login Failed'})


@app.route('/api/v1/skater_page')
def skater_page():
    if 'user_id' in session:
        db_skater = term.query(Skater).get(session['user_id'])

        skater = {'id': db_skater.id, 'name': db_skater.name,
        'tag': db_skater.tag,
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
        for spot in db_skater.spots]}

        return jsonify(skater)
    else:
        return jsonify({'Error': 'Please Sign Up or Log In to Create a Profile'})

@app.route('/api/v1/new_spot', methods=['POST'])
def post_spot():
    if 'user_id' in session:
        spot_json = json.loads(request.data)

        spot = SkateSpot(name=spot_json['name'],
        description=spot_json['description'],
        street_name=spot_json['street_name'],
        latitude=float(spot_json['latitude']),
        longitude=float(spot_json['longitude']),
        skater_id=session['user_id'])

        term.add(spot)
        term.commit()

        photo = Photo(url=spot_json['photo_url'],
        spot_id=spot.id)

        term.add(photo)
        term.commit()

        def boolean(rating = spot_json['rating']):
            if rating == 'True':
                return True
            else:
                return False

        favorite = Favorites(skater_id=session['user_id'],
        spot_id=spot.id, rating=boolean())

        term.add(favorite)
        term.commit()

        return redirect(url_for('skater_page'))
    else:
        return jsonify({'Error': 'Sign Up or Log In To Post Spots'})

if __name__ == '__main__':
    app.run(debug=True)
