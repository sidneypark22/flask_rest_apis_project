from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import current_app, render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import or_
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from models import StoreModel, ItemModel
from blocklist import BLOCKLIST

from resources.store import Store

blp = Blueprint('Web', 'web', description='web')

@blp.route('/')
@blp.route('/hello')
@blp.route('/hello/<user>')
def hello_world(user=None):
    user = user or 'Sidney'
    return render_template('index.html', user=user)

@blp.route('/home')
def home():
    stores = StoreModel.query.order_by(StoreModel.name).all()
    return render_template('home.html', stores=stores)

@blp.route('/home/store/<store_id>/item/', methods=['GET', 'POST'])
def item(store_id):
    if request.method == 'GET':
        items = ItemModel.query.filter(ItemModel.store_id==store_id).order_by(ItemModel.price.asc())
        return render_template('item.html', items=items, store_id=store_id)

@blp.route('/home/store/<store_id>/item/delete/<item_id>', methods=['GET', 'POST'])
def item_delete(store_id, item_id):
    if request.method == 'POST':
        if request.form['item_submit'] == 'Delete Item':
            item = ItemModel.query.get_or_404(item_id)
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for('Web.item', store_id=store_id))
        #return render_template('index.html', user=request.form['item_submit'])
        #return redirect(request.url)

@blp.route('/home/store/<store_id>/item/add', methods=['GET', 'POST'])
def item_add(store_id):
    if request.method == 'POST':
        if request.form['item_submit'] == 'Add Item':
            item_data = {
                "name": request.form.get('item_add_name'),
                "price": request.form.get('item_add_price'),
                "store_id": store_id,
                "description": request.form.get('item_add_desc')
            }
            item = ItemModel(**item_data)
            
            try:
                db.session.add(item)
                db.session.commit()
                return redirect(url_for('Web.item', store_id=store_id))
            except SQLAlchemyError:
                abort(500, message='An error occurred while inserting the item.')


#def get_items(store_id):
#    items = ItemModel.query.filter(ItemModel.store_id==store_id).order_by(ItemModel.price.asc())
#    return render_template('item.html', items=items)
#def action():
#    if request.method == 'DELETE':
#        render_template('index.html', user=request.form)
#def delete():
#    if request.form['item_submit'] == 'Delete Item':
#        item_id = request.form['id']
#        print(item_id)
#        print('YASSSSSS!!!!')
#    #item = ItemModel.query.get_or_404(item_id)
#    #db.session.delete(item)
#    #db.session.commit()
#    return render_template('item.html')

#def delete_item(item_id):
#    def delete():


#PRODUCTS = {
#    'iphone': {
#        'name': 'iPhone 5S',
#        'category': 'Phones',
#        'price': 699,
#    },
#    'galaxy': {
#        'name': 'Samsung Galaxy 5',
#        'category': 'Phones',
#        'price': 649,
#    },
#    'ipad-air': {
#        'name': 'iPad Air',
#        'category': 'Tablets',
#        'price': 649,
#    },
#    'ipad-mini': {
#        'name': 'iPad Mini',
#        'category': 'Tablets',
#        'price': 549
#    }
#}
#
#@blp.route('/home')
#def home():
#    return render_template('home.html', products=PRODUCTS)
#
#@blp.route('/product/<key>')
#def product(key):
#    product = PRODUCTS.get(key)
#    if not product:
#        abort(404)
#    return render_template('product.html', product=product)
#
#@blp.route('/list_products')
#def list_products():
#    return PRODUCTS

