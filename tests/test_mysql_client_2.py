import unittest
from datetime import datetime
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.db.models.subscription import Subscription, Base, engine, session
from service.db.mysql_client_2 import create_subscription, modify_subscription, delete_subscription, get_subscription_details

class TestSubscriptionClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the database and create tables
        Base.metadata.create_all(engine)

    def setUp(self):
        # Add sample data for testing
        sample_subscription = Subscription(
            user_id=101,
            product_id=201,
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 12, 31),
            status='active'
        )
        session.add(sample_subscription)
        session.commit()

    def tearDown(self):
        # Remove sample data after each test
        session.query(Subscription).delete()
        session.commit()

    def test_create_subscription(self):
        request_data = {
            "user_id": 102,
            "product_id": 202,
            "start_date": datetime(2023, 2, 1),
            "end_date": datetime(2023, 12, 31),
            "status": 'active'
        }

        response = create_subscription(request_data)
        self.assertEqual(response.user_id, 102)
        # Add more assertions based on your schema

    def test_modify_subscription(self):
        request_data = {
            "user_id": 103,
            "product_id": 203,
            "start_date": datetime(2023, 3, 1),
            "end_date": datetime(2023, 12, 31),
            "status": "inactive"
        }
        response = modify_subscription(request_data)
        self.assertEqual(response.user_id, 103)
        self.assertEqual(response.status, 'inactive')
        # Add more assertions based on your schema

    # def test_delete_subscription(self):
    #     request_data = {"subscription_id": 1}
    #     response = delete_subscription(request_data)
    #     self.assertIsNone(response)
    #     deleted_subscription = session.query(Subscription).get(1)
    #     self.assertIsNone(deleted_subscription)

    # def test_get_subscription_details(self):
    #     request_data = {"subscription_id": 1}
    #     response = get_subscription_details(request_data)
    #     self.assertIsNotNone(response)
    #     self.assertEqual(response.subscription_id, 1)
    #     self.assertEqual(response.user_id, 101)
    #     # Add more assertions based on your schema

if __name__ == '__main__':
    unittest.main()
