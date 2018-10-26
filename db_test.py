import db_test_models
import unittest
from IPython import embed

class TestDatabaseRelations(unittest.TestCase):
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

        photo1 = db_test_models.Photo(url='http://www.nullozinejr.com/zine/wp-content/uploads/2015/01/IMG_20150111_094308.jpg',
        spot_id=spot1.id)

        photo2 = db_test_models.Photo(url='http://www.nullozinejr.com/zine/wp-content/uploads/2015/01/IMG_20150111_101845.jpg',
        spot_id=spot1.id)

        photo3 = db_test_models.Photo(url='http://www.nullozinejr.com/zine/wp-content/uploads/2015/01/IMG_20150111_101734.jpg',
        spot_id=spot1.id)

        photo4 = db_test_models.Photo(url='http://www.sundrymourning.com/wp-content/uploads/2006/12/121506_porta.jpg',
        spot_id=spot2.id)

        session.add_all([photo1, photo2, photo3, photo4])
        session.commit()

        favorite1 = db_test_models.Favorites(skater_id=dood1.id,
        spot_id=spot1.id, rating=True)

        favorite2 = db_test_models.Favorites(skater_id=dood1.id,
        spot_id=spot2.id, rating=True)

        favorite3 = db_test_models.Favorites(skater_id=dood2.id,
        spot_id=spot2.id, rating=False)

        session.add_all([favorite1, favorite2, favorite3])
        session.commit()

        self.assertEqual(dood1.id, spot1.skater_id)
        self.assertEqual(dood2.id, spot2.skater_id)
        self.assertEqual(spot1.photos, [photo1, photo2, photo3])
        self.assertEqual(spot2.photos, [photo4])
        self.assertEqual(spot1.favorites, [favorite1])
        self.assertEqual(spot2.favorites, [favorite2, favorite3])
        self.assertTrue(spot1.favorites[0].rating)
        self.assertTrue(spot2.favorites[0].rating)
        self.assertFalse(spot2.favorites[1].rating)
        self.assertEqual(spot1.skaters, [dood1])
        self.assertEqual(spot2.skaters, [dood1, dood2])
        self.assertEqual(dood1.favorites, [favorite1, favorite2])
        self.assertEqual(dood2.favorites, [favorite3])
        self.assertEqual(dood1.favorite_spots, [spot1, spot2])
        self.assertEqual(dood2.favorite_spots, [spot2])
        self.assertEqual(photo1.spot_id, spot1.id)
        self.assertEqual(photo2.spot_id, spot1.id)
        self.assertEqual(photo3.spot_id, spot1.id)
        self.assertEqual(photo4.spot_id, spot2.id)
    db_test_models.drop_db

if __name__ == '__main__':
    unittest.main()
