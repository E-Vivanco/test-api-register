from models import User, Profile
from flask import Flask
from flask import Blueprint, jsonify, request
from config import DevelopmentConfig
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db,  User, Profile

bpProfile = Blueprint('bpProfile', __name__)
app = Flask(__name__)
jwt = JWTManager(app)

@bpProfile.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:    
            id = get_jwt_identity()

            user = User.query.get(id)
            return jsonify(user.serialize_profile()), 200
    except Exception as e:
            return jsonify({"msg":"falla lectura de profile"})

@bpProfile.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
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
    except Exception as e:
            return jsonify({"msg":"no se logro actualizar profile"})
