from flask import Flask, render_template, request, redirect, url_for
import grpc
from service.protos import subscription_pb2_grpc
from service.protos.subscription_pb2 import SubscriptionRequest

app = Flask(__name__)

# gRPC connection setup
channel = grpc.insecure_channel('localhost:50051')
stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_subscription', methods=['POST'])
def fetch_subscription():
    subscription_id = int(request.form['subscription_id'])

    # gRPC request
    request_data = SubscriptionRequest(subscription_id=subscription_id)
    response = stub.GetSubscriptionDetails(request_data)

    # Pass the response to the template
    return render_template('result.html', subscription=response)

@app.route('/create_subscription', methods=['GET', 'POST'])
def create_subscription():
    if request.method == 'POST':
        subscription_id = int(request.form['subscription_id'])

        # gRPC request to create a new subscription
        request_data = SubscriptionRequest(subscription_id=subscription_id)
        response = stub.CreateSubscription(request_data)

        # Redirect to a page displaying the newly created subscription
        return redirect(url_for('fetch_subscription', subscription_id=subscription_id))

    return render_template('create_subscription.html')

if __name__ == '__main__':
    app.run(debug=True)
