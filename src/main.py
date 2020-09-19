"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Job_Post
from sqlalchemy import Column, ForeignKey, Integer, String
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['JWT_SECRET_KEY'] = 'b85536e15f59b519eaf4dac6c3cde80bc87d39438f52a1b5e7933d6fffea8836'  # Change this!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

########## CREATE-ACCOUNT ENDPOINT - POST - used to create a user account
@app.route('/create-account', methods=['POST'])
def create_user():

    if request.method == 'POST':
        body = request.get_json()
        print(body)
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "first_name" not in body:
            raise APIException('You need to specify the first name', status_code=400)
        if "last_name" not in body:
            raise APIException('You need to specify the last name', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in body:
            raise APIException('You need to specify the password', status_code=400)
        if 'address' not in body:
            raise APIException('You need to specify the address', status_code=400)
        if 'zipcode' not in body:
            raise APIException('You need to specify the zipcode', status_code=400)
        if 'sex' not in body:
            raise APIException('You need to specify the sex of the user', status_code=400)
        if 'type_of_user' not in body:
            raise APIException('You need to specify the type of user', status_code=400)
        
        user1 = User(first_name=body['first_name'], last_name=body['last_name'], password = body['password'], email = body['email'], address=body['address'], zipcode = body['zipcode'], sex = body['sex'], type_of_user= body['type_of_user'])
            
        db.session.add(user1)
        db.session.commit()

        return "ok", 200

########## GET ALL USERS ENDPOINT - GET - shows all users who have an account
@app.route('/user', methods=['GET'])
def get_user():
    if request.method == 'GET':
        all_user = User.query.all()
        all_user = list(map(lambda x: x.serialize(), all_user))
        return jsonify(all_user), 200

    return "Invalid Method", 404

########## GET SINGLE USER ENDPOINT - GET, PUT, DELETE
@app.route('/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_single_user(user_id):
    if request.method == 'GET':
        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(user1.serialize()), 200

# PUT request - updates the user's account info
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)

        if "first_name" in body:
            user1.name = body["first_name"]
        if "last_name" in body:
            user1.name = body["last_name"]
        if "email" in body:
            user1.email = body["email"]
        if "password" in body:
            user1.password = body["password"]
        if "address" in body:
            user1.zipcode = body["address"]
        if "sex" in body:
            user1.sex = body["sex"]
        if "zipcode" in body:
            user1.zipcode = body["zipcode"]
        if "type_of_user" in body:
            user1.zipcode = body["type_of_user"]
        db.session.commit()

        return jsonify(user1.serialize()), 200

# DELETE request - delete's the user's account
    if request.method == 'DELETE':
        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(user1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


########## LOG-IN ENDPOINT - used for logging in
@app.route('/login', methods=['POST', 'PUT'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)
    # type_of_user = params.get('type_of_user', None)
    if not email:
        return jsonify({"msg": "Missing email in request"}), 400
    if not password:
        return jsonify({"msg": "Missing password in request"}), 400

    # check for "type_of_user" in database
    type_of_user = 'job-poster'
    usercheck = User.query.filter_by(email=email, password=password).first()
    if usercheck is None:
        # type_of_user = 'job-seeker'
        usercheck = Job-Seeker.query.filter_by(email=email, password=password).first()

    # if user not found
    if usercheck == None:
        return jsonify({"msg": "Invalid credentials provided"}), 401

    #if user found, Identity can be any data that is json serializable
    ret = {
        # 'jwt': create_jwt(identity=email), <---- Will not work if un-commented
        'user': usercheck.serialize()
    }
    return jsonify(ret), 200

# PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)

        if "first_name" in body:
            user1.name = body["first_name"]
        if "last_name" in body:
            user1.name = body["last_name"]
        if "email" in body:
            user1.email = body["email"]
        if "password" in body:
            user1.password = body["password"]
        if "address" in body:
            user1.zipcode = body["address"]
        if "sex" in body:
            user1.sex = body["sex"]
        if "zipcode" in body:
            user1.zipcode = body["zipcode"]
        if "type_of_user" in body:
            user1.zipcode = body["type_of_user"]
        db.session.commit()

        return jsonify(user1.serialize()), 200


########## JOB-POST ENDPOINTS
@app.route('/job-post', methods=['POST', 'GET'])
def get_job_post():

########## Create a job-post
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'job_title' not in body:
            raise APIException('You need to specify the job title', status_code=400)
        if 'job_description' not in body:
            raise APIException('You need to specify the job description', status_code=400)
        if 'job_address' not in body:
            raise APIException('You need to specify the job address', status_code=400)
        if 'job_zipcode' not in body:
            raise APIException('You need to specify the zipcode', status_code=400)

        job1 = Job_Post(job_title=body['job_title'], job_description = body['job_description'], job_address = body['job_address'], job_zipcode = body['job_zipcode'])
        db.session.add(job1)
        db.session.commit()

        return "ok", 200

########## View all job-posts
    if request.method == 'GET':
        all_job = Job_Post.query.all()
        all_job = list(map(lambda x: x.serialize(), all_job))
        return jsonify(all_job), 200

    return "Invalid Method", 404

 

########## SINGLE JOB POST ENDPOINT - GET, PUT, DELETE
@app.route('/job_post/<int:job_post_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_job_post(job_id):
    """
    Single job post
    """
########## View single job-post
    if request.method == 'GET':
        job1 = Job.query.get(job_id)
        if job1 is None:
            raise APIException('Job not found', status_code=404)
        return jsonify(job1.serialize()), 200

########## Update single job-post
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        job1 = Job.query.get(job_id)
        if job1 is None:
            raise APIException('Job not found', status_code=404)

        if "job_title" in body:
            job1.job_title = body["job_title"]
        if "job_description" in body:
            job1.job_description = body["job_description"]
        if "job_address" in body:
            job1.address = body["job_address"]
        if "job_zipcode" in body:
            job1.job_zipcode = body["job_zipcode"]
        db.session.commit()

        return jsonify(job1.serialize()), 200  

########## Delete single job-post
    if request.method == 'DELETE':
        job1 = Job.query.get(job_id)
        if job1 is None:
            raise APIException('Job not found', status_code=404)
        db.session.delete(job1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

################################################################################################################################################################

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
