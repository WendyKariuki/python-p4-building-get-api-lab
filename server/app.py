from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood
from sqlalchemy import desc, func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [{'id': bakery.id, 'name': bakery.name, 'created_at': str(bakery.created_at)} for bakery in bakeries]
    return jsonify(bakery_list)

@app.route('/bakeries/<int:id>')
def get_bakery(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        baked_goods = [{'id': good.id, 'name': good.name, 'price': good.price, 'created_at': str(good.created_at)} for good in bakery.baked_goods]
        bakery_info = {'id': bakery.id, 'name': bakery.name, 'baked_goods': baked_goods, 'created_at': str(bakery.created_at)}
        return jsonify(bakery_info)
    else:
        return jsonify({'error': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    baked_goods_list = [{'id': good.id, 'name': good.name, 'price': good.price, 'created_at': str(good.created_at)} for good in baked_goods]
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(desc(BakedGood.price)).first()
    if most_expensive_good:
        return jsonify({'id': most_expensive_good.id, 'name': most_expensive_good.name, 'price': most_expensive_good.price, 'created_at': str(most_expensive_good.created_at)})
    else:
        return jsonify({'error': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
