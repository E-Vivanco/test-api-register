import os
import datetime
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from models import db,  User, Profile

load_dotenv()

app = Flask(__name__)
app.config['DEBUG']=True
app.config['ENV']='development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] ="cualquier_palabra"
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)
CORS(app)


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def main():
    return jsonify({ "message": "Welcome to my API REST Flask" }), 200

#
@app.route('/api/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    if not email: return jsonify({"message": "Email is required"}), 400
    if not password: return jsonify({"message": "Password is required"}), 400

    foundUser = User.query.filter_by(email=email).first()
    
    if not foundUser: return jsonify({"message": "Email/Password are incorrects"}), 401
    if not check_password_hash(foundUser.password, password): return jsonify({"message": "Email/Password are incorrects"}), 401


    expires = datetime.timedelta(days=3)
    access_token = create_access_token(identity=foundUser.id, expires_delta=expires)

    data = {
        "access_token": access_token,
        "user": foundUser.serialize()
    }

    return jsonify(data), 200

@app.route('/api/register', methods=['POST'])
def register():
    
    email = request.json.get('email')
    password = request.json.get('password')
    biography = request.json.get('biography', "")
    linkedin = request.json.get('linkedin', "")
    github = request.json.get('github', "")

    if not email: return jsonify({"message": "Email is required"}), 400
    if not password: return jsonify({"message": "Password is required"}), 400

    foundUser = User.query.filter_by(email=email).first()
    if foundUser: return jsonify({"message": "Email already exists"}), 400

    user = User()

    user.email = email
    user.password = generate_password_hash(password)

    profile = Profile()
    profile.biography = biography
    profile.linkedin = linkedin
    profile.github = github

    user.profile = profile
    user.save()

    if user:
        expires = datetime.timedelta(days=3)
        access_token = create_access_token(identity=user.id, expires_delta=expires)

        data = {
            "access_token": access_token,
            "user": user.serialize()
        }

        return jsonify(data), 201

    return jsonify({ "message": "Please try again later."}), 400





@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    id = get_jwt_identity()

    user = User.query.get(id)
    return jsonify(user.serialize_profile()), 200

@app.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    id = get_jwt_identity()

    biography = request.json.get('biography')
    linkedin = request.json.get('linkedin')
    github = request.json.get('github')

    user = User.query.get(id)

    user.profile.biography = biography
    user.profile.linkedin = linkedin
    user.profile.github = github

    user.update()

    return jsonify(user.serialize_profile()), 200
if __name__ == '__main__':
   app.run()