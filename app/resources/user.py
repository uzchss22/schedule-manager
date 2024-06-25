from flask import Blueprint, request
from flask_restful import Api, Resource
from app import db
from app.models import User
from flask_jwt_extended import create_access_token

bp = Blueprint('user', __name__)
api = Api(bp)

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User registered successfully."}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials."}, 401

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
