import grpc
from service.db.mysql_client import MySQLClient, MySQLError
from service.protos import subscription_pb2
from service.protos.subscription_pb2_grpc import SubscriptionServiceServicer
import datetime
from google.protobuf.timestamp_pb2 import Timestamp

import logging

from service.subscription import Subscription

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Reuse database connections
dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "Database@1990",
    "database": "virendra_meena"
}

class SubscriptionServicer(SubscriptionServiceServicer):

    def __init__(self):
        self.mysql_client = MySQLClient(dbconfig)

    def CreateSubscription(self, request, context):
        try:
            subscription = Subscription(
                subscription_id=0,  # Auto incremented
                user_id=request.user_id,
                product_id=request.product_id,
                start_date=request.start_date.ToDatetime(),
                end_date=request.end_date.ToDatetime(),
                status=get_status(request.status)
            )

            self.mysql_client.create_subscription(subscription)

            # Retrieve auto-generated id
            result = self.mysql_client.get_subscription(
                subscription.subscription_id)
            subscription.subscription_id = result[0]

            return subscription.to_proto()

        except MySQLError as e:
            context.set_details(f"MySQL error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return subscription_pb2.SubscriptionResponse()

    def DeleteSubscription(self, request, context):
        try:
            self.mysql_client.delete_subscription(request.subscription_id)
            return subscription_pb2.SubscriptionResponse(
                subscription_id=request.subscription_id
            )

        except MySQLError as e:
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
                status=get_status(request.status)
            )

            self.mysql_client.update_subscription(subscription)

            return subscription.to_proto()

        except MySQLError as e:
            context.set_details(f"MySQL error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return subscription_pb2.SubscriptionResponse()

    def GetSubscriptionDetails(self, request, context):
        logger.info(f"Received GetSubscriptionDetails request: {request}")
        # Your existing code here
        # fetch subscription details from mysql client using subscription_id of request.

        try:
            subscription = self.mysql_client.get_subscription(
                request.subscription_id)
        except MySQLError as e:
            # Set gRPC error details and code
            context.set_details(f'Failed to get subscription: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)

            # Return empty response
            return subscription_pb2.SubscriptionResponse()

        if not subscription:
            # Subscription not found
            context.set_details(
                f'Subscription with id {request.subscription_id} not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return subscription_pb2.SubscriptionResponse()

        # Create and return response from subscription object
        return subscription.to_proto()


def get_status(status_value):
    if status_value == 1:
        return "INACTIVE"
    else:
        return "ACTIVE"
