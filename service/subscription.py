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
  
  @classmethod
  def from_proto(cls, request : subscription_pb2.SubscriptionRequest):
    return cls(
      subscription_id=request.subscription_id,
      user_id=request.user_id,
      product_id=request.product_id,
      start_date=request.start_date.ToDatetime(),
      end_date=request.end_date.ToDatetime(),
      status=request.status
    )
  

  def to_proto(self) -> subscription_pb2.SubscriptionResponse:
    response = subscription_pb2.SubscriptionResponse()
    response.subscription_id = self.subscription_id
    response.user_id = self.user_id
    response.product_id = self.product_id
    response.start_date.FromDatetime(self.start_date)
    response.end_date.FromDatetime(self.end_date)
    response.status = self.status
    return response
