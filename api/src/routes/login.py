from models import User, Profile
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

bpLogin = Blueprint('bpLogin', __name__)

@bpLogin.route('/api/login', methods=['POST'])
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

@bpLogin.route('/api/register', methods=['POST'])
def register():
    
    email = request.json.get('email')
    password = request.json.get('password')
    biography = request.json.get('biography', "")
    linkedin = request.json.get('linkedin', "")
    github = request.json.get('github', "")
    facebook = request.json.get('facebook', "")

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
    profile.facebook = facebook

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

