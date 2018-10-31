import db_models
from werkzeug.security import generate_password_hash, check_password_hash
from IPython import embed

engine = db_models.engine

db_models.Base.metadata.drop_all(engine)

db_models.Base.metadata.create_all(engine)

session = db_models.Session()

password1 = generate_password_hash('baller420')
password2 = generate_password_hash('bulletHead666')

dood1 = db_models.Skater(name='Dod Gobson', tag='Skate Hard, Die Young',
email='www.skate_dood1@thrasher_mag.com', password=password1)

dood2 = db_models.Skater(name='Johnny Razors', tag='Embrace fire!',
email='www.skate_dood2@thrasher_mag.com', password=password2)

session.add_all([dood1, dood2])
session.commit()

spot1 = db_models.SkateSpot(description='Loads of stairs, tons of rails',
name='Some Campus', latitude=14.123456,
longitude=44.456123, skater_id=dood1.id)

spot2 = db_models.SkateSpot(description='Tipped over porta throne',
name='Hell', latitude=12.123456,
longitude=40.456123, skater_id=dood2.id)

session.add_all([spot1, spot2])
session.commit()

photo1 = db_models.Photo(url='http://www.nullozinejr.com/zine/wp-content/uploads/2015/01/IMG_20150111_094308.jpg',
spot_id=spot1.id)

photo2 = db_models.Photo(url='http://www.nullozinejr.com/zine/wp-content/uploads/2015/01/IMG_20150111_101845.jpg',
spot_id=spot1.id)

photo3 = db_models.Photo(url='http://www.nullozinejr.com/zine/wp-content/uploads/2015/01/IMG_20150111_101734.jpg',
spot_id=spot1.id)

photo4 = db_models.Photo(url='http://www.sundrymourning.com/wp-content/uploads/2006/12/121506_porta.jpg',
spot_id=spot2.id)

session.add_all([photo1, photo2, photo3, photo4])
session.commit()

favorite1 = db_models.Favorites(skater_id=dood1.id,
spot_id=spot1.id, rating=True)

favorite2 = db_models.Favorites(skater_id=dood1.id,
spot_id=spot2.id, rating=True)

favorite3 = db_models.Favorites(skater_id=dood2.id,
spot_id=spot2.id, rating=False)

session.add_all([favorite1, favorite2, favorite3])
session.commit()
