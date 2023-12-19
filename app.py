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

    # Get subscription details from form
    user_id = int(request.form['user_id'])
    product_id = int(request.form['product_id'])  
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    status = request.form['status']

    # gRPC request
    request_data = SubscriptionRequest(
        user_id=user_id,
        product_id=product_id,
        start_date=start_date, # TODO: convert to timestamp
        end_date=end_date, # TODO: convert to timestamp
        status=status
    )
    response = stub.GetSubscriptionDetails(request_data)

    # Pass the response to the template
    return render_template('result.html', subscription=response)

@app.route('/create_subscription', methods=['GET', 'POST'])
def create_subscription():
    if request.method == 'POST':
        # Get subscription details from form
        user_id = int(request.form['user_id'])
        product_id = int(request.form['product_id'])  
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        status = request.form['status']

        # gRPC request
        request_data = SubscriptionRequest(
            user_id=user_id,
            product_id=product_id,
            start_date=start_date, # TODO: convert to timestamp
            end_date=end_date, # TODO: convert to timestamp
            status=status
        )
        
        response = stub.CreateSubscription(request_data)

        # Pass the response to the template
        return render_template('result.html', subscription=response)

    return render_template('create_subscription.html')

if __name__ == '__main__':
    app.run(debug=True)
