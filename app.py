from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
import os
import secrets
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
from blocklist import BLOCKLIST
import models

from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from datetime import timedelta

def create_app(db_url=None, testing: bool = True):
    app = Flask(__name__)
    load_dotenv()

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = 'Stores REST API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL', 'sqlite:///data.db') #If not found, default to second argument
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = '334879676493251022500810511667956218385'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    # This should be something secure in the real world
    # Generate it using secrets.SystemRandom().getrandbits(128)
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(
            {
                "description": "The token has been revoked.",
                "error": "token_revoked"
            }
        ), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required"
            }
        ), 401

    # You can add a bit more information to the jwt by using claim.
    # This tutor does not use claim much though.
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Proper way should be to look int the database and see whether the user is an admin
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(
            {
                "message": "The token has expired.",
                "error": "token_expired."
            }
        ), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify(
            {
                "message": "Signature varification failed.", 
                "error": "invalid_token"
            }
        ), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(
            {
                "description": "Request doesn not contain an access token.",
                "error": "authorization_required" 
            }
        ), 401

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    app.config

    return app




### Below codes have been moved to blupritns under resources folder.

#@app.route('/store', methods=['GET', 'POST']) #http://127.0.0.1:5000/store
#def all_stores():
#    if request.method == 'GET':
#        #return {"stores": list[stores.values()]}
#        #return "Hello World"
#        return {"stores": list(stores.values())}
#    elif request.method == 'POST':
#        new_store_data = request.get_json()
#        if 'name' not in new_store_data:
#            abort(
#                400,
#                message="Bad request. Ensure 'name' is included in the JSON payload."
#            )
#        new_store_id = uuid.uuid4().hex
#        new_store = {
#            **new_store_data, 
#            "id": new_store_id
#        }
#        stores[new_store_id] = new_store
#        return new_store, 201 # 201 means okay and accepte
#
#
#@app.route('/store/<string:store_id>', methods=['GET', 'DELETE'])
#def store(store_id):
#    if request.method == 'GET':
#        try:
#            return stores[store_id]
#        except:
#            abort(404, message="Store not found")
#    elif request.method == 'DELETE':
#        try:
#            del stores[store_id]
#            return {"message": "Store deleted."}
#        except KeyError:
#            abort(
#                404,
#                message="Store not found."
#            )
#
#
#@app.route('/item', methods=['GET', 'POST'])
#def all_items():
#    if request.method == 'GET':
#        return {"items": list(items.values())}
#    elif request.method == 'POST':
#        new_item_data = request.get_json()
#        if (
#            "price" not in new_item_data or
#            "store_id" not in new_item_data or
#            "name" not in new_item_data
#        ):
#            abort(
#                400,
#                message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload."
#            )
#        for item in items.values():
#            if (
#                new_item_data['name'] == item['name'] and
#                new_item_data['store_id'] == item['store_id']
#            ):
#                abort(404, message="Item already exists.")
#        if new_item_data["store_id"] not in stores:
#            return {"message": "Store not found"}, 404
#        new_item_id = uuid.uuid4().hex
#        new_item = {
#            **new_item_data,
#            "id": new_item_id
#        }
#        items[new_item_id] = new_item
#        return new_item, 201
#
#
#@app.route('/item/<string:item_id>', methods=['GET', 'DELETE', 'PUT'])
#def item(item_id):
#    if request.method == 'GET':
#        try:
#            return items[item_id]
#        except KeyError:
#            abort(404, message="Store not found")
#    if request.method == 'DELETE':
#        try:
#            del items[item_id]
#            return {"message": "Store deleted."}
#        except KeyError:
#            abort(
#                404,
#                message="Item not found."
#            )
#    if request.method == 'PUT':
#        item_data = request.get_json()
#        if 'price' not in item_data or 'name' not in item_data:
#            abort(
#                400,
#                message="Bad request. Ensure 'price' and 'name' are included in the JSON payload."
#            )
#        try:
#            item = items[item_id]
#            item |= item_data
#            return item
#        except KeyError:
#            abort(
#                404,
#                message="Item not found."
#            )
#
##    for store in stores:
##        if request.method == 'GET':
##            if store['name'] == name:
##                return {
##                    "items": store['items'],
##                    "message": "You rock!"
##                }
##        if request.method == 'POST':
##            request_data = request.get_json()
##            for store in stores:
##                if store['name'] == name:
##                    new_item = {
##                        "name": request_data["name"],
##                        "price": request_data["price"]
##                    }
##                    store["items"].append(new_item)
##                    return new_item, 201
##    return {"message": "Store not found"}, 404
