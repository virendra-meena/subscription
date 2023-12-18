import grpc
from service.db.mysql_client import MySQLClient
from service.protos import subscription_pb2
from service.protos.subscription_pb2_grpc import SubscriptionServiceServicer
import datetime
from google.protobuf.timestamp_pb2 import Timestamp 

import logging

from service.subscription import Subscription, create_subscription_response

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SubscriptionServicer(SubscriptionServiceServicer):

    def __init__(self):
        self.mysql_client = MySQLClient()

    def CreateSubscription(self, request, context):
        try:
            subscription = Subscription(
                subscription_id=0, # Auto incremented
                user_id=request.user_id,
                product_id=request.product_id,
                start_date=request.start_date.ToDatetime(),
                end_date=request.end_date.ToDatetime(),
                status=request.status
            )

            self.mysql_client.create_subscription(subscription)

            # Retrieve auto-generated id
            result = self.mysql_client.get_subscription(subscription.subscription_id)
            subscription.subscription_id = result[0]

            return create_subscription_response(subscription)
        
        except self.mysql_client.Error as e:
            context.set_details(f"MySQL error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return subscription_pb2.SubscriptionResponse()

    def DeleteSubscription(self, request, context):
        try:
            self.mysql_client.delete_subscription(request.subscription_id)
            return subscription_pb2.SubscriptionResponse(
                subscription_id=request.subscription_id
            )

        except self.mysql_client.Error as e:
            context.set_details(f"MySQL error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return subscription_pb2.SubscriptionResponse()

    def ModifySubscription(self, request, context):
        try:
            subscription = Subscription(
                subscription_id=request.subscription_id,
                user_id=request.user_id,
                product_id=request.product_id,
                start_date=request.start_date.ToDatetime(),
                end_date=request.end_date.ToDatetime(),
                status=request.status
            )

            self.mysql_client.update_subscription(subscription)
            
            return create_subscription_response(subscription)

        except self.mysql_client.Error as e:
            context.set_details(f"MySQL error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return subscription_pb2.SubscriptionResponse()

    def GetSubscriptionDetails(self, request, context):
        logger.info(f"Received GetSubscriptionDetails request: {request}")
        # Your existing code here
        # fetch subscription details from mysql client using subscription_id of request.
        
        try:
            subscription = self.mysql_client.get_subscription_by_id(request.subscription_id)
        except MySQLClient.Error as e:
            # Set gRPC error details and code
            context.set_details(f'Failed to get subscription: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)
            
            # Return empty response
            return subscription_pb2.SubscriptionResponse()

        if not subscription:
            # Subscription not found
            context.set_details(f'Subscription with id {request.subscription_id} not found') 
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return subscription_pb2.SubscriptionResponse()

        # Create and return response from subscription object
        response = create_subscription_response(subscription)
        return response



def create_dummy_subscription_response():

  response = subscription_pb2.SubscriptionResponse()

  response.subscription_id = get_dummy_subscription_id()
  response.user_id = get_dummy_user_id()
  response.product_id = get_dummy_product_id()
  
  response.start_date.CopyFrom(get_dummy_start_date())
  response.end_date.CopyFrom(get_dummy_end_date())

  response.status = get_dummy_status()

  return response

def get_dummy_subscription_id():
  return 123

def get_dummy_user_id():
  return 456

def get_dummy_product_id():
  return 789

def get_dummy_start_date():
  start_date = Timestamp()
  start_date.FromDatetime(datetime.datetime(2020, 1, 1))
  return start_date

def get_dummy_end_date():
  end_date = Timestamp()
  end_date.FromDatetime(datetime.datetime(2020, 12, 31))
  return end_date  

def get_dummy_status():
  return subscription_pb2.ACTIVE