from models import User, Profile
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

bpUsers = Blueprint('bpUsers', __name__)

@bpUsers.route('/api/users', methods=['GET'])
def all_users():

    users = User.query.all()  # [<User 1>, <User 2>]
    users = list(map(lambda user: user.serialize_profile(), users))

    return jsonify(users), 200
