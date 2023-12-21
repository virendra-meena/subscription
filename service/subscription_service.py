import grpc

from db.mysql_client import create_subscription, delete_subscription, modify_subscription, get_subscription_details
from service.protos import subscription_pb2
from service.protos.subscription_pb2 import Status
from service.protos.subscription_pb2_grpc import SubscriptionServiceServicer
from datetime import datetime, timezone
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.json_format import MessageToDict

import logging

from service.db.models.subscription import Subscription

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def log_function_errors(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Error in function {func.__name__}: {str(e)}")
                raise e

        return wrapper

    return decorator

class SubscriptionServicer(SubscriptionServiceServicer):

    def CreateSubscription(self, request, context):
        try:
            subscription_request_dict = MessageToDict(request, preserving_proto_field_name=True)
            response = create_subscription(subscription_request_dict)
     
            return convert_to_proto(response)

        except Exception as e:
            context.set_details(f"MySQL error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return subscription_pb2.SubscriptionResponse()

    def DeleteSubscription(self, request, context):
        try:
            subscription_request_dict = MessageToDict(request, preserving_proto_field_name=True)
            response = delete_subscription(subscription_request_dict)
            return convert_to_proto(response)
        
        except Exception as e:
            context.set_details(f"MySQL error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return subscription_pb2.SubscriptionResponse()

    def ModifySubscription(self, request, context):
        try:
            subscription_request_dict = MessageToDict(request, preserving_proto_field_name=True)
            response =  modify_subscription(subscription_request_dict)
            return convert_to_proto(response)

        except Exception as e:
            context.set_details(f"MySQL error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return subscription_pb2.SubscriptionResponse()

    def GetSubscriptionDetails(self, request, context):
        logger.info(f"Received GetSubscriptionDetails request: {request}")
        # Your existing code here
        # fetch subscription details from mysql client using subscription_id of request.

        try:
            subscription_request_dict = MessageToDict(request, preserving_proto_field_name=True)
            response = get_subscription_details(subscription_request_dict)
            return convert_to_proto(response)

        except Exception as e:
            # Set gRPC error details and code
            context.set_details(f'Failed to get subscription: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)

            # Return empty response
            return subscription_pb2.SubscriptionResponse()


# Apply the decorator to your function
@log_function_errors(logger)
def convert_to_proto(subscription):
    # Create a SubscriptionRequest instance
    subscription_proto = subscription_pb2.SubscriptionResponse()

    # Populate SubscriptionRequest fields from Subscription instance
    subscription_proto.subscription_id = subscription.subscription_id
    subscription_proto.user_id = subscription.user_id
    subscription_proto.product_id = subscription.product_id

    # Convert datetime fields to google.protobuf.Timestamp
# Convert date to datetime 
    subscription_proto.start_date.FromDatetime(
        datetime.combine(subscription.start_date, datetime.min.time()).astimezone(timezone.utc)
    )

    subscription_proto.end_date.FromDatetime(
        datetime.combine(subscription.end_date, datetime.min.time()).astimezone(timezone.utc)  
    )


    # Map Enum field 'status'
    if subscription.status == 'active':
        subscription_proto.status = Status.active
    elif subscription.status == 'inactive':
        subscription_proto.status = Status.inactive

    return subscription_proto