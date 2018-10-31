from flask import Flask, request, render_template, jsonify, redirect, url_for, session, abort
from db_models import SkateSpot, Skater, Photo, Favorites
from IPython import embed
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ
import db_models
import json
import os

app = Flask(__name__)

secret_key = environ.get('SECRET_KEY')

app.config['SECRET_KEY'] = secret_key

term = db_models.Session()

@app.route('/')
def hello():
    return 'SKATEBOARDING IS NOT A CRIME'

@app.route('/api/v1/spots')
def get_spots():
    skater_spots = term.query(SkateSpot).all()

    spots = [{'id': spot.id, 'name': spot.name,
    'description': spot.description,
    'latitude': spot.latitude,
    'longitude': spot.longitude,
    'skater_id': spot.skater_id,
    'photos': [{'url': photo.url} for photo in spot.photos]}
    for spot in skater_spots]

    return jsonify(spots)


@app.route('/api/v1/spots/<int:id>')
def get_spot(id=1):
    skater_spot = term.query(SkateSpot).get(id)

    if skater_spot != None:
        spot = {'id': skater_spot.id, 'name': skater_spot.name,
        'description': skater_spot.description,
        'latitude': skater_spot.latitude,
        'longitude': skater_spot.longitude,
        'skater_id': skater_spot.skater_id,
        'photos': [{'url': photo.url} for photo in skater_spot.photos]}
    else:
        abort(404)
    return jsonify(spot)

@app.route('/api/v1/skaters', methods=['GET'])
def request_skaters():
    skaters = term.query(Skater).all()

    dudes = [{'id': skater.id, 'name': skater.name,
    'tag': skater.tag,
    'skate_spots': [{'id': spot.id, 'name': spot.name,
    'description': spot.description,
    'latitude': spot.latitude,
    'longitude': spot.longitude,
    'skater_id': spot.skater_id,
    'photos': [{'url': photo.url} for photo in spot.photos]}
    for spot in skater.spots]}
    for skater in skaters]

    return jsonify(dudes)

@app.route('/api/v1/skaters/<int:id>')
def get_skater(id=1):
    skater = term.query(Skater).get(id)

    if skater != None:
        dude = {'id': skater.id, 'name': skater.name,
        'tag': skater.tag,
        'skate_spots': [{'id': spot.id, 'name': spot.name,
        'description': spot.description,
        'latitude': spot.latitude,
        'longitude': spot.longitude,
        'skater_id': spot.skater_id,
        'photos': [{'url': photo.url} for photo in spot.photos]}
        for spot in skater.spots]}
    else:
        abort(404)

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
        abort(406)
    else:
        skater_json = json.loads(request.data)
        skater = term.query(Skater).filter(Skater.name == skater_json['name'])

        if not skater.all():
            abort(406)
        else:
            if check_password_hash(skater[0].password, skater_json['password']) == True:
                session['user_id'] = skater[0].id

                return redirect(url_for('skater_page'))
            else:
                abort(406)

@app.route('/api/v1/skater_page')
def skater_page():
    if 'user_id' in session:
        db_skater = term.query(Skater).get(session['user_id'])

        skater = {'id': db_skater.id, 'name': db_skater.name,
        'tag': db_skater.tag,
        'skate_spots': [{'id': spot.id, 'name': spot.name,
        'description': spot.description,
        'latitude': spot.latitude,
        'longitude': spot.longitude,
        'skater_id': spot.skater_id,
        'photos': [{'url': photo.url} for photo in spot.photos]}
        for spot in db_skater.spots]}

        return jsonify(skater)
    else:
        abort(403)

@app.route('/api/v1/update_skater', methods=['PATCH'])
def update_skater():
    if 'user_id' in session:
        skater_json = json.loads(request.data)
        password = generate_password_hash(skater_json['password'])

        term.query(Skater).filter(Skater.id == session['user_id']).update({Skater.name: skater_json['name'],
        Skater.email: skater_json['name'], Skater.tag: skater_json['tag'],
        Skater.password: password}, synchronize_session=False)
        term.commit

        return redirect(url_for('skater_page'))
    else:
        abort(403)

@app.route('/api/v1/new_spot', methods=['POST'])
def post_spot():
    if 'user_id' in session:
        spot_json = json.loads(request.data)

        spot = SkateSpot(name=spot_json['name'],
        description=spot_json['description'],
        latitude=float(spot_json['latitude']),
        longitude=float(spot_json['longitude']),
        skater_id=session['user_id'])

        term.add(spot)
        term.commit()

        photo = Photo(url=spot_json['photo_url'],
        spot_id=spot.id)

        term.add(photo)
        term.commit()

        return redirect(url_for('skater_page'))
    else:
        abort(403)

@app.route('/api/v1/update_spot/<int:id>', methods=['PATCH'])
def update_spot(id):
    if 'user_id' in session:
        spot_json = json.loads(request.data)

        term.query(SkateSpot).filter(SkateSpot.id == id).update({SkateSpot.name: spot_json['name'],
        SkateSpot.description: spot_json['description']}, synchronize_session=False)
        term.commit

        return redirect(f'/api/v1/spots/{id}')
    else:
        abort(406)

@app.route('/api/v1/delete_spot/<int:id>', methods=['DELETE'])
def delete_spot(id):
    if 'user_id' in session:
        photos = term.query(Photo).filter(Photo.spot_id == id)
        spot = term.query(SkateSpot).get(id)

        if spot.skater_id == session['user_id']:
            for photo in photos.all():
                term.delete(photo)
            term.delete(spot)
            term.commit()

            return jsonify({'Success': 'The Selected Spot has Been Deleted'})
        else:
            abort(403)
    else:
        abort(403)

@app.route('/api/v1/logout')
def logout_skater():
    session.pop('user_id', None)
    return jsonify({'Success': 'You are logged out'})

if __name__ == '__main__':
    app.run()
