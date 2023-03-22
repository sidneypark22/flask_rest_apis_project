from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from db import db
from sqlalchemy.exc import SQLAlchemyError

from models import ItemModel
from schema import ItemSchema, ItemUpdateSchema

blp = Blueprint('Items', __name__, description='Operations on items')

@blp.route('/item/<int:item_id>')
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get('is_admin'):
            abort(401, message='Admin privilege required.')
        
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}
    
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)# not get_or_404 because we still want to return None if not exists
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route('/item')
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True) # This means you will need a fresh token to perform this action. You typically do this for change passwords, deleting account etc.
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occurred while inserting the item.')
        
        return item

        ### item_data argument above now covers this
        #new_item_data = request.get_json()
        ### Now validation is done by Marshmellow
        #if (
        #    "price" not in new_item_data or
        #    "store_id" not in new_item_data or
        #    "name" not in new_item_data
        #):
        #    abort(
        #        400,
        #        message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload."
        #    )


        #for item in items.values():
        #    if (
        #        item_data['name'] == item['name'] and
        #        item_data['store_id'] == item['store_id']
        #    ):
        #        abort(404, message="Item already exists.")
        #if item_data["store_id"] not in stores:
        #    return {"message": "Store not found"}, 404
        #new_item_id = uuid.uuid4().hex
        #new_item = {
        #    **item_data,
        #    "id": new_item_id
        #}
        #items[new_item_id] = new_item
        #return new_item, 201
