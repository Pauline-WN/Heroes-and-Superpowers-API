import unittest
from app import create_app, db  # Removed redundant db import
from app.models import Hero, Power, HeroPower

class APITestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test app and test client
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for tests
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()

        # Create database tables and test data
        with self.app.app_context():
            db.create_all()  # Create tables

            # Add some sample heroes and powers
            hero1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
            power1 = Power(name="flight", description="Ability to fly")
            db.session.add(hero1)
            db.session.add(power1)
            db.session.commit()

    def tearDown(self):
        # Clean up database after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()  # Drop all tables

    def test_get_heroes(self):
        # Test the GET /heroes route
        response = self.client.get('/heroes')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_hero_by_id(self):
        # Test the GET /heroes/:id route
        response = self.client.get('/heroes/1')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Kamala Khan")

    def test_get_non_existent_hero(self):
        # Test the GET /heroes/:id route for a non-existent hero
        response = self.client.get('/heroes/999')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

    def test_create_hero_power(self):
        # Test POST /hero_powers to create a new HeroPower
        hero_data = {
            "strength": "Average",
            "power_id": 1,
            "hero_id": 1
        }
        with self.app.app_context():  
            response = self.client.post('/hero_powers', json=hero_data)
            data = response.get_json()
            self.assertEqual(response.status_code, 201)
            self.assertIn('strength', data)
            self.assertEqual(data['strength'], "Average")

if __name__ == '__main__':
    unittest.main()
