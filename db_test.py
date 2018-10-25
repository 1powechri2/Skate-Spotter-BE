import db_test_models
import unittest
from IPython import embed

class TestDatabaseFunctions(unittest.TestCase):
    db_test_models.migrate_db

    def test_create_spot(self):
        session = db_test_models.Session()

        dood1 = db_test_models.Skater(name='Dod', tag='Skate, OverDose, Die')

        dood2 = db_test_models.Skater(name='Gob', tag='Eat rats!')

        session.add_all([dood1, dood2])
        session.commit()

        spot1 = db_test_models.SkateSpot(description='Big Ramp',
        name='Hell', street_name='666 rock st.', latittude=12.123456,
        longitude=40.456123, skater_id=dood1.id)

        spot2 = db_test_models.SkateSpot(description='Big Ramp',
        name='Hell', street_name='666 rock st.', latittude=12.123456,
        longitude=40.456123, skater_id=dood2.id)

        session.add_all([spot1, spot2])
        session.commit()

        photo1 = db_test_models.Photo(url='www.skateordie.com/thrasher',
        spot_id=spot1.id)

        photo2 = db_test_models.Photo(url='www.skateordied.com/thrasher',
        spot_id=spot1.id)

        photo3 = db_test_models.Photo(url='www.skateordies.com/thrasher',
        spot_id=spot1.id)

        photo4 = db_test_models.Photo(url='www.skateordiediedie.com/thrasher',
        spot_id=spot2.id)

        session.add_all([photo1, photo2, photo3, photo4])
        session.commit()

        favorite1 = db_test_models.Favorites(skater_id=dood1.id,
        spot_id=spot1.id, rating=True)

        favorite2 = db_test_models.Favorites(skater_id=dood1.id,
        spot_id=spot1.id, rating=True)

        favorite3 = db_test_models.Favorites(skater_id=dood2.id,
        spot_id=spot2.id, rating=True)

        session.add_all([favorite1, favorite2, favorite3])
        session.commit()

        self.assertEqual(dood1.id, spot1.skater_id)
        self.assertEqual(dood2.id, spot2.skater_id)
    db_test_models.drop_db

if __name__ == '__main__':
    unittest.main()
