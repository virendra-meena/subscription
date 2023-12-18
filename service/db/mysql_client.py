import mysql.connector
from mysql.connector import pooling

# Reuse database connections 
dbconfig = {
  "host":"localhost",
  "user":"root",
  "password":"Database@1990",
  "database":"virendra_meena"
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
  pool_name = "database_pool",
  pool_size = 5,
  **dbconfig
)

# Prepare statements
insert_subscription = "INSERT INTO subscription (user_id, product_id, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)"
get_subscription = "SELECT subscription_id, status FROM subscription WHERE subscription_id=%s" 
update_subscription  = "UPDATE subscription SET user_id=%s, product_id=%s, start_date=%s, end_date=%s, status=%s WHERE subscription_id=%s"

class MySQLClient:

  def __init__(self):
    self.conn = connection_pool.get_connection() 
    self.cursor = self.conn.cursor(prepared=True)

  # Batch queries    
  def batch_execute(self, queries):
    self.cursor.execute("START TRANSACTION")
    for query in queries:
      self.cursor.execute(query)
    self.cursor.execute("COMMIT")

  def create_subscription(self, subscription):
    params = (subscription.user_id, subscription.product_id, 
              subscription.start_date, subscription.end_date, subscription.status)
    self.cursor.execute(insert_subscription, params)

  def get_subscription(self, subscription_id):
    self.cursor.execute(get_subscription, (subscription_id,))
    return self.cursor.fetchone()    

  def update_subscription(self, subscription):
    params = (subscription.user_id, subscription.product_id,  
              subscription.start_date, subscription.end_date, 
              subscription.status, subscription.subscription_id)
    self.cursor.execute(update_subscription, params)

# Return connection to pool  
def __del__(self):
  self.conn.close()
