from flask import Flask, render_template, request, redirect, url_for
import grpc
from service.protos import subscription_pb2_grpc
from service.protos.subscription_pb2 import SubscriptionRequest, Status
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

app = Flask(__name__)

# gRPC connection setup
channel = grpc.insecure_channel('localhost:50051')
stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_subscription', methods=['POST'])
def fetch_subscription():

    request_data = SubscriptionRequest()
    request_data.user_id = int(request.form['user_id'])if request.form['user_id'] else None
    if 'product_id' in request.form:
        request_data.product_id = int(request.form['product_id']) if request.form['product_id'] else None
    
    if 'start_date' in request.form:
        request_data.start_date.FromDatetime(datetime.datetime.strptime(request.form['start_date'], "%Y-%m-%d"))
    if 'end_date' in request.form:
        request_data.end_date.FromDatetime(datetime.datetime.strptime(request.form['end_date'], "%Y-%m-%d"))
    
    if 'status' in request.form:
        request_data.status = Status.ACTIVE if request.form['status'] == "active" else Status.INACTIVE

    response = stub.GetSubscriptionDetails(request_data)

    # Pass the response to the template
    return render_template('result.html', subscription=response)

@app.route('/create_subscription', methods=['GET', 'POST'])
def create_subscription():
    if request.method == 'POST':

        request_data = SubscriptionRequest()
        request_data.user_id = int(request.form['user_id']) if request.form['user_id'] else None
        if 'product_id' in request.form:
            request_data.product_id = int(request.form['product_id']) if request.form['product_id'] else None
        
        if 'start_date' in request.form:
            request_data.start_date.FromDatetime(datetime.datetime.strptime(request.form['start_date'], "%Y-%m-%d"))
        if 'end_date' in request.form:
            request_data.end_date.FromDatetime(datetime.datetime.strptime(request.form['end_date'], "%Y-%m-%d"))
        
        if 'status' in request.form:
            request_data.status = Status.ACTIVE if request.form['status'] == "active" else Status.INACTIVE
        
        response = stub.CreateSubscription(request_data)

        # Pass the response to the template
        return render_template('result.html', subscription=response)

    return render_template('create_subscription.html')

if __name__ == '__main__':
    app.run(debug=True)
