# flask imports
from flask import request, jsonify, make_response, Blueprint
# from  werkzeug.security import generate_password_hash, check_password_hash

# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os
from project import db
from project.models import User

auth = Blueprint('auth', __name__)

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, os.environ.get('SECRET_KEY'))
            current_user = User.query\
                .filter_by(email = data['email'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated

  
# route for logging user in
@auth.route('/login', methods =['POST'])
def login():
    # creates dictionary of form data
    data = request.get_json()
  
    if not data or not data['email'] or not data['password']:
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = User.query\
        .filter_by(email = data['email'])\
        .first()
  
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
  
    if user.password == data['password']:
        # generates the JWT Token
        token = jwt.encode({
            'email': user.email,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, os.environ.get('SECRET_KEY'))
  
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )
  
# signup route
@auth.route('/signup', methods =['POST'])
def signup():
    # gets name, email and password
    data = request.get_json()
    print(data)
    name = data['name']
    email = data['email']
    mobile = data['phone-number']
    password = data['password']
    print(name, email, password, mobile)
    # checking for existing user
    user = User.query\
        .filter_by(email = email)\
        .first()
    if not user:
        # database ORM object
        user = User(
            name = name,
            email = email,
            mobile = mobile,
            password = password
        )
        # insert user
        db.session.add(user)
        db.session.commit()
  
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)