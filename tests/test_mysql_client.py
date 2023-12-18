import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.subscription import Subscription
from service.db.mysql_client import MySQLClient
import unittest
from datetime import datetime


"""
Tests for MySQLClient database interactions.

This module contains unit tests for the MySQLClient class which handles
interactions with the MySQL database for the subscription service.

Classes:

TestMySQLClient
    Main test class that inherits from unittest.TestCase.

    Methods:
    
    setUp()
        Creates a MySQLClient instance for tests to use.

    tearDown()
        Cleans up test data by deleting all rows from the 
        subscription table after each test.

    test_create_and_get_subscription()
        Tests creating a new subscription and retrieving it.
        Creates a sample Subscription object and inserts it
        using the MySQLClient. Then fetches the subscription
        using MySQLClient and verifies the status.

    test_update_subscription()
        Tests updating an existing subscription.
        Creates a subscription, updates the status via MySQLClient,
        and verifies the status was updated by retrieving it.

The tests should be run using:

python -m unittest Tests.test_mysql_client

This allows the tests to be discovered and run.

Individual tests can be run using:

python -m unittest Tests.test_mysql_client.TestMySQLClient.test_method

Where test_method is the name of the specific test case.
"""

class TestMySQLClient(unittest.TestCase):

    def setUp(self):
        self.client = MySQLClient()

    def tearDown(self):
        # Clean up data after each test
        self.client.cursor.execute("DELETE FROM subscription")

    def test_create_and_get_subscription(self):
        sub = Subscription(
            user_id=1,
            product_id=2,
            start_date=datetime(2020, 1, 1),
            end_date=datetime(2020, 12, 31),
            status='active'
        )
        self.client.create_subscription(sub)

        result = self.client.get_subscription(sub.subscription_id)
        self.assertEqual(result[1], 'active')

    # def test_update_subscription(self):
    #     # Create subscription
    #     sub = Subscription(
    #         user_id=1,
    #         product_id=2,
    #         start_date=datetime(2020, 1, 1),
    #         end_date=datetime(2020, 12, 31),
    #         status='active'
    #     )
    #     self.client.create_subscription(sub)

    #     # Update status
    #     sub.status = 'inactive'
    #     self.client.update_subscription(sub)

    #     # Verify update
    #     result = self.client.get_subscription(sub.subscription_id)
    #     self.assertEqual(result[1], 'inactive')

    # Add other test cases


if __name__ == '__main__':


    unittest.main()
