import unittest

from rooms import ApartmentChairsCounter

from .test_data import (test_corners, test_full_bathroom, test_no_chairs,
                        test_outisde, test_room)

ROOM = test_room

class TestApartmentChairsCounter(unittest.TestCase):

    def setUp(self) -> None:
        # Initialize ApartmentChairsCounter instance

        self.apartment_chairs_counter = ApartmentChairsCounter(ROOM.get('path'))
        self.apartment_chairs_counter.count_chairs()

    def test_parse_apartment_plan(self):
        # Test parsing of apartment file
        apartment_plan = self.apartment_chairs_counter.parse_apartment_plan()
        self.assertIsInstance(self.apartment_chairs_counter.apartment_plan, str)
    
    def test_total(self):
        # test total chairs in appartment
        total = self.apartment_chairs_counter.apartment_chairs.get('total')
        test_total = ROOM['rooms']['total']

        self.assertEqual(total, test_total)

    def test_balcony(self):
        # test nr. of chairs on balcony
        balcony = self.apartment_chairs_counter.apartment_chairs.get('balcony')
        test_balcony = ROOM['rooms']['balcony']

        self.assertEqual(test_balcony, balcony)

    def test_bathroom(self):
        # test nr of chairs in bathroom
        bathroom = self.apartment_chairs_counter.apartment_chairs.get('bathroom')
        test_bathroom = ROOM['rooms']['bathroom']

        self.assertEqual(test_bathroom, bathroom)

    def test_closet(self):
        # test nr. of chairs in closet
        closet = self.apartment_chairs_counter.apartment_chairs.get('closet')
        test_closet = ROOM['rooms']['closet']
        self.assertEqual(test_closet, closet)

    def test_kitchen(self):
        # test nr. of chairs in kitchen
        kitchen = self.apartment_chairs_counter.apartment_chairs.get('kitchen')
        test_kitchen = ROOM['rooms']['kitchen']
        self.assertEqual(test_kitchen, kitchen)

    def test_living_rooms(self):
        # test nr. of chairs in living room
        living_room = self.apartment_chairs_counter.apartment_chairs.get('living room')
        test_living_room = ROOM['rooms']['living room']
        self.assertEqual(test_living_room, living_room)
    
    def test_office(self):
        # test nr. of chair in office
        office = self.apartment_chairs_counter.apartment_chairs.get('office')
        test_office = ROOM['rooms']['office']
        self.assertEqual(test_office, office)

    def test_sleeping_room(self):
        # test nr. of chairs in sleep room
        sleeping_room = self.apartment_chairs_counter.apartment_chairs.get('sleeping room')
        test_sleeping = ROOM['rooms']['sleeping room']
        self.assertEqual(test_sleeping, sleeping_room)

    def test_toilet(self):
        # test nr. of chair in toilet
        toilet = self.apartment_chairs_counter.apartment_chairs.get('toilet')
        test_toilete = ROOM['rooms']['toilet']
        self.assertEqual(test_toilete, toilet)

    def test_rooms_order(self):
        # test alpfabetical order of rooms
        self.assertEqual(list(ROOM['rooms'].keys()), ['total', 'balcony', 'bathroom', 'closet', 'kitchen', 'living room', 'office', 'sleeping room', 'toilet'])



                

if __name__ == '__main__':
    unittest.main()