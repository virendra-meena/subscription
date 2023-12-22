from flask import Flask, render_template, request, redirect, url_for, session
import grpc
from flask_oauthlib.client import OAuth, OAuthRemoteApp
from service.protos import subscription_pb2_grpc
from service.protos.subscription_pb2 import SubscriptionRequest, Status
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

app = Flask(__name__)
app.secret_key = 'subscription@1990'  # Change this to a strong, random key

# gRPC connection setup
channel = grpc.insecure_channel('localhost:50051')
stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)

# OAuth configuration for Google Sign-In
oauth = OAuth(app)
# google = oauth.remote_app(
#     'google',
#     consumer_key="312190595659-g00t00mvim46a6ma7llkqtauol8dk5ml.apps.googleusercontent.com",
#     consumer_secret="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",
#     request_token_params={'scope': 'email profile'},
#     base_url='https://www.googleapis.com/plus/v1/',
#     request_token_url=None,
#     access_token_method='POST',
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
# )

google = OAuthRemoteApp(
    oauth,
    'google',
    consumer_key="312190595659-g00t00mvim46a6ma7llkqtauol8dk5ml.apps.googleusercontent.com",
    consumer_secret="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",
    request_token_params={'scope': 'email profile'},
    base_url='https://www.googleapis.com/plus/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',  
)

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')
    return 'Logged in as: ' + user_info.data['name']

# # Callback to load user info from the session
# @oauth.tokengetter
# def get_google_oauth_token():
#     return session.get('google_token')


# Index route - Check if user is logged in
@app.route('/')
def index():
    if 'google_token' in session:
        return 'Logged in as: ' + session['google_email']
    return 'You are not logged in.'

# Google Sign-In route
@app.route('/login/google')
def login_google():
    return google.authorize(callback=url_for('authorized_google', _external=True))

# Callback route for handling Google authorization
@app.route('/login/google/callback')
def authorized_google():
    response = google.authorized_response()

    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    # Get user info from Google API
    user_info = google.get('people/me')

    # Extract user data as needed
    user_id = user_info.data['id']
    user_email = user_info.data['emails'][0]['value']

    # Store user info or perform user registration as needed
    # You can use user_id and user_email to identify users
    session['google_token'] = (response['access_token'], '')
    session['google_email'] = user_email

    return redirect(url_for('index'))

@app.route('/fetch_subscription', methods=['POST'])
def fetch_subscription():
    if 'google_token' not in session:
        return redirect(url_for('login_google'))

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
    if 'google_token' not in session:
        return redirect(url_for('login_google'))
        
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
