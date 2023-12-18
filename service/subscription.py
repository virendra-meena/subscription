# service/subscription.py

from datetime import datetime
from service.db.mysql_client import MySQLClient
from service.protos import subscription_pb2

class Subscription:

  def __init__(self, subscription_id, user_id, product_id, start_date, end_date, status):
    self.subscription_id = subscription_id
    self.user_id = user_id 
    self.product_id = product_id
    self.start_date = start_date
    self.end_date = end_date  
    self.status = status

  @classmethod
  def from_db(cls, result):
    return cls(
      subscription_id=result[0],
      user_id=result[1],
      product_id=result[2],
      start_date=result[3],
      end_date=result[4],
      status=result[5]  
    )

def create_subscription_response(subscription):
  response = subscription_pb2.SubscriptionResponse()
  response.subscription_id = subscription.subscription_id
  response.user_id = subscription.user_id
  response.product_id = subscription.product_id
  response.start_date.FromDatetime(subscription.start_date)
  response.end_date.FromDatetime(subscription.end_date)
  response.status = subscription.status
  return response
