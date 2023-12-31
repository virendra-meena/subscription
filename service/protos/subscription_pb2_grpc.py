# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from service.protos import subscription_pb2 as protos_dot_subscription__pb2


class SubscriptionServiceStub(object):
    """Define the service with APIs for subscription operations
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateSubscription = channel.unary_unary(
                '/subscription.SubscriptionService/CreateSubscription',
                request_serializer=protos_dot_subscription__pb2.SubscriptionRequest.SerializeToString,
                response_deserializer=protos_dot_subscription__pb2.SubscriptionResponse.FromString,
                )
        self.DeleteSubscription = channel.unary_unary(
                '/subscription.SubscriptionService/DeleteSubscription',
                request_serializer=protos_dot_subscription__pb2.SubscriptionRequest.SerializeToString,
                response_deserializer=protos_dot_subscription__pb2.SubscriptionResponse.FromString,
                )
        self.ModifySubscription = channel.unary_unary(
                '/subscription.SubscriptionService/ModifySubscription',
                request_serializer=protos_dot_subscription__pb2.SubscriptionRequest.SerializeToString,
                response_deserializer=protos_dot_subscription__pb2.SubscriptionResponse.FromString,
                )
        self.GetSubscriptionDetails = channel.unary_unary(
                '/subscription.SubscriptionService/GetSubscriptionDetails',
                request_serializer=protos_dot_subscription__pb2.SubscriptionRequest.SerializeToString,
                response_deserializer=protos_dot_subscription__pb2.SubscriptionResponse.FromString,
                )


class SubscriptionServiceServicer(object):
    """Define the service with APIs for subscription operations
    """

    def CreateSubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteSubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModifySubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSubscriptionDetails(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SubscriptionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateSubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateSubscription,
                    request_deserializer=protos_dot_subscription__pb2.SubscriptionRequest.FromString,
                    response_serializer=protos_dot_subscription__pb2.SubscriptionResponse.SerializeToString,
            ),
            'DeleteSubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteSubscription,
                    request_deserializer=protos_dot_subscription__pb2.SubscriptionRequest.FromString,
                    response_serializer=protos_dot_subscription__pb2.SubscriptionResponse.SerializeToString,
            ),
            'ModifySubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.ModifySubscription,
                    request_deserializer=protos_dot_subscription__pb2.SubscriptionRequest.FromString,
                    response_serializer=protos_dot_subscription__pb2.SubscriptionResponse.SerializeToString,
            ),
            'GetSubscriptionDetails': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSubscriptionDetails,
                    request_deserializer=protos_dot_subscription__pb2.SubscriptionRequest.FromString,
                    response_serializer=protos_dot_subscription__pb2.SubscriptionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'subscription.SubscriptionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SubscriptionService(object):
    """Define the service with APIs for subscription operations
    """

    @staticmethod
    def CreateSubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/subscription.SubscriptionService/CreateSubscription',
            protos_dot_subscription__pb2.SubscriptionRequest.SerializeToString,
            protos_dot_subscription__pb2.SubscriptionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteSubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/subscription.SubscriptionService/DeleteSubscription',
            protos_dot_subscription__pb2.SubscriptionRequest.SerializeToString,
            protos_dot_subscription__pb2.SubscriptionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ModifySubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/subscription.SubscriptionService/ModifySubscription',
            protos_dot_subscription__pb2.SubscriptionRequest.SerializeToString,
            protos_dot_subscription__pb2.SubscriptionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSubscriptionDetails(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/subscription.SubscriptionService/GetSubscriptionDetails',
            protos_dot_subscription__pb2.SubscriptionRequest.SerializeToString,
            protos_dot_subscription__pb2.SubscriptionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
