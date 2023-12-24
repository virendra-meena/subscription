from flask import Flask, render_template, request, redirect, url_for, session
import grpc
from flask_oauthlib.client import OAuth, OAuthRemoteApp
from service.protos import subscription_pb2_grpc
from service.protos.subscription_pb2 import SubscriptionRequest, Status
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
import logging

app = Flask(__name__)
app.secret_key = 'subscription@1990'  # Change this to a strong, random key

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# gRPC connection setup
channel = grpc.insecure_channel('localhost:50051')
stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)

# OAuth configuration for Google Sign-In
oauth = OAuth(app)

# google = oauth.remote_app(
#     'google',
#     consumer_key="312190595659-g00t00mvim46a6ma7llkqtauol8dk5ml.apps.googleusercontent.com",
#     consumer_secret="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",
#     request_token_params={'scope': "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"},
#     base_url='https://www.googleapis.com/plus/v1/',
#     request_token_url=None,
#     access_token_method='POST',
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     authorize_url='https://accounts.google.com/o/oauth2/auth',  
# )

google = oauth.remote_app(
    'google',
    consumer_key="312190595659-g00t00mvim46a6ma7llkqtauol8dk5ml.apps.googleusercontent.com",
    consumer_secret="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",
    request_token_params={'scope': "email profile"},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Additional configuration for the userinfo endpoint
google.userinfo = 'https://www.googleapis.com/oauth2/v1/userinfo'

# Callback to load user info from the session
@google.tokengetter
def get_google_oauth_token(token=None):
    logging.debug(f"OAuth token retrieved: {token}")
    return session.get('google_token')

# Index route - Check if user is logged in
@app.route('/')
def index():
    if 'google_token' in session:
        return render_template('home.html', email=session.get('google_email'))
    return render_template('index.html')

# Home route - Display welcome page
@app.route('/home')
def home():
    if 'google_token' not in session:
        return redirect(url_for('login_google'))
    return render_template('home.html', email=session.get('google_email', 'Unknown'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract user registration data
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']

        # Perform user registration logic here

        # Redirect to home or login page after registration
        return redirect(url_for('index'))

    # Render the registration form for GET requests
    return render_template('register.html')

# Logout route - Log the user out
@app.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('google_email', None)
    return redirect(url_for('index'))

# generic Sign-in route
@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    logging.debug(f"Initiating OAuth flow. Callback URL: {callback}")
    return google.authorize(callback=callback)

# Google Sign-In route
@app.route('/login/google')
def login_google():
    callback = url_for('authorized_google', _external=True)
    logging.debug(f"Initiating Google OAuth flow. Callback URL: {callback}")
    return google.authorize(callback=callback, prompt='select_account')

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    logging.debug(f"OAuth response: {resp}")
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('people/me')
    #user_info = google.get('https://www.googleapis.com/userinfo/v2/me')
    return 'Logged in as: ' + user_info.data['name']

# Callback route for handling Google authorization
@app.route('/login/google/callback')
def authorized_google():
    logging.debug(f"google object info: {google}")
    response = google.authorized_response()
    logging.debug(f"Google OAuth response: {response}")

    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    # # Get user info from Google API
    user_info = google.get('https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses')
    logging.debug(f"Google user info: {user_info.data}")

    # # Extract user data as needed
            # Extract the email from user_info
    user_email = user_info.data.get('emailAddresses', [{}])[0].get('value', '')

    # Store user info or perform user registration as needed
    # You can use user_id and user_email to identify users
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
