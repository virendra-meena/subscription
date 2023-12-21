import grpc
from service.db.mysql_client import MySQLClient, MySQLError
from service.db.mysql_client_2  import create_subscription, delete_subscription, modify_subscription, get_subscription_details
from service.protos import subscription_pb2
from service.protos.subscription_pb2_grpc import SubscriptionServiceServicer
import datetime
from google.protobuf.timestamp_pb2 import Timestamp

import logging

from service.subscription import Subscription

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SubscriptionServicer(SubscriptionServiceServicer):

    def CreateSubscription(self, request, context):
        try:
            return create_subscription(request)

        except Exception as e:
            context.set_details(f"MySQL error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return subscription_pb2.SubscriptionResponse()

    def DeleteSubscription(self, request, context):
        try:
            return delete_subscription(request)

        except Exception as e:
            context.set_details(f"MySQL error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return subscription_pb2.SubscriptionResponse()

    def ModifySubscription(self, request, context):
        try:
            return modify_subscription(request)

        except Exception as e:
            context.set_details(f"MySQL error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return subscription_pb2.SubscriptionResponse()

    def GetSubscriptionDetails(self, request, context):
        logger.info(f"Received GetSubscriptionDetails request: {request}")
        # Your existing code here
        # fetch subscription details from mysql client using subscription_id of request.

        try:
            return get_subscription_details(request)
        
        except Exception as e:
            # Set gRPC error details and code
            context.set_details(f'Failed to get subscription: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)

            # Return empty response
            return subscription_pb2.SubscriptionResponse()
