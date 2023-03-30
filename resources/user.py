from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import current_app
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import or_
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from models import UserModel
from schema import UserSchema, UserRegisterSchema
from blocklist import BLOCKLIST

from tasks import send_user_registration_email

blp = Blueprint('Users', 'users', description='Operations on users')

@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username==user_data['username'],
                UserModel.email==user_data['email']
            )
        ).first():
            abort(409, message='A user with that username or email already exists.')

        user = UserModel(
            username=user_data['username'],
            email=user_data['email'],
            password=pbkdf2_sha256.hash(user_data['password'])
        )
        #try:
        #    db.session.add(user)
        #    db.session.commit()
        #    
        #    current_app.queue.enqueue(send_user_registration_email, user.email, user.username)
        #
        #except IntegrityError:
        #    abort(400, message='A user with that name already exists.')
        #except SQLAlchemyError:
        #    abort(500, message='An error occurred while registering the user.')
        
        db.session.add(user)
        db.session.commit()
            
        current_app.queue.enqueue(send_user_registration_email, user.email, user.username)

        return {"message": "User created successfully."}, 201


@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data['username']
        ).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        
        abort(401, 'Invalid credentials.')

@blp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh=True) #this means it needs refresh token, not access token
    def post(self):
        current_user = get_jwt_identity() #returns None if there is no current user
        new_token = create_access_token(identity=current_user, fresh=False) #if fresh True, then it will refresh the refresh token too
        ## Do this to generate only one fresh token for every refresh token
        #jti = get_jwt()['jti']
        #BLOCKLIST.add(jti)

        return {"access_token": new_token}

@blp.route('/logout')
class UserLotout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {
            "message": "Successfully logged out."
        }
        

@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200

