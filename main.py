import grpc
from concurrent import futures
from service.protos import subscription_pb2_grpc
from service.subscription_service import SubscriptionServicer
import logging

def serve():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    subscription_pb2_grpc.add_SubscriptionServiceServicer_to_server(SubscriptionServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()