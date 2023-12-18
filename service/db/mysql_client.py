"""
MySQL client for subscription service.

This module handles interactions with the MySQL database for the 
subscription service, including CRUD operations on the subscriptions
table.

Classes:

MySQLClient
    Wrapper for managing MySQL connections and queries.

    Methods:

    __init__()
        Initializes the MySQL connection pool and prepared statements.
        Also configures logging.

    batch_execute()
        Executes a batch of queries as a transaction.

    create_subscription()
        Inserts a new subscription record.

    get_subscription()
        Fetches a subscription by id.

    update_subscription()
        Updates an existing subscription record.

    __del__()
        Closes the MySQL connection and returns it to the pool.

The main external interface is the MySQLClient class. This handles 
connecting to MySQL, preparing statements, and executing queries.

The database connection pool is created on startup for reusing 
connections efficiently. 

Prepared statements are used for all queries to protect against
SQL injection.

Parameters are passed as arguments rather than interpolating query strings.

All database errors are handled and logged.
"""

import logging
import mysql.connector
from mysql.connector import pooling

# Reuse database connections
dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "Database@1990",
    "database": "virendra_meena"
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="database_pool",
    pool_size=5,
    **dbconfig
)

# Prepare statements
insert_subscription = "INSERT INTO subscription (user_id, product_id, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)"
get_subscription = "SELECT subscription_id, status FROM subscription WHERE subscription_id=%s"
update_subscription = "UPDATE subscription SET user_id=%s, product_id=%s, start_date=%s, end_date=%s, status=%s WHERE subscription_id=%s"


class MySQLClient:

    def __init__(self):
        self.conn = connection_pool.get_connection()
        self.cursor = self.conn.cursor(prepared=True)

        # Set up logging
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    # Batch queries
    def batch_execute(self, queries):
        try:
            self.cursor.execute("START TRANSACTION")
            for query in queries:
                self.cursor.execute(query)
            self.cursor.execute("COMMIT")
        except Exception as e:
            self.logger.error("Error executing batch queries: %s", e)
            raise

    def create_subscription(self, subscription):
        try:
            params = (subscription.user_id, subscription.product_id,
                      subscription.start_date, subscription.end_date, subscription.status)
            self.cursor.execute(insert_subscription, params)
        except Exception as e:
            self.logger.error("Error creating subscription: %s", e)
            raise

    def get_subscription(self, subscription_id):
        try:
            self.cursor.execute(get_subscription, (subscription_id,))
            return self.cursor.fetchone()
        except Exception as e:
            self.logger.error("Error getting subscription: %s", e)
            raise

    def update_subscription(self, subscription):
        try:
            params = (subscription.user_id, subscription.product_id,
                      subscription.start_date, subscription.end_date,
                      subscription.status, subscription.subscription_id)
            self.cursor.execute(update_subscription, params)
        except Exception as e:
            self.logger.error("Error updating subscription: %s", e)
            raise

    # Return connection to pool
    def __del__(self):
        self.conn.close()
