#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()

    response = make_response(
        bakery_serialized,
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

@app.route('/baked_goods', methods=["GET", "POST", "DELETE"])
def baked_goods():
    if request.method == "GET":
        all_cakes = []
        cakes = BakedGood.query.all()
        for cake in cakes:
            cake_dict = cake.to_dict()
            all_cakes.append(cake_dict)

        response1 = make_response(jsonify(all_cakes), 200)
        
        
        return response1

    elif request.method == "POST":
        new_baked = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            created_at=request.form.get("created_at"),
            updated_at=request.form.get("updated_at"),
            bakery_id=request.form.get("bakery_id")
        )
        db.session.add(new_baked)
        db.session.commit()

        review_dict = new_baked.to_dict()
        response2 = make_response(jsonify(review_dict), 201)  # Update the status code to 201
        response2.headers["Content-Type"] = "application/json"
        
        
        return response2

@app.route('/baked_goods/<int:id>',methods=["GET","PATCH","DELETE",])
def delete_baked_goods(id):
    single_baked_good=BakedGood.query.filter_by(id=id).first()
    if request.method=="GET":
        single_baked_good_dict=single_baked_good.to_dict()
        response1=make_response(jsonify(single_baked_good_dict),200)
        response1.headers["Content-Type"]="application/json"
       
       
        return response1
    
    elif request.method=="PATCH":
        for attribute in request.form:
            setattr(attribute,single_baked_good,request.form.get(attribute))
        db.session.commit()
        single_baked_good_dict2=single_baked_good.to_dict()
        response3=make_response(jsonify(d=single_baked_good_dict2),200)
        response3.headers["Content-Type"]="application/json"
       
       
        return response3


    elif request.method=="DELETE":
        db.session.delete(single_baked_good)
        db.session.commit()

        response_body = {
                "delete_successful": True,
                "message": "Review deleted."
            }
        response2=make_response(jsonify(response_body),200)
        response2.headers["Content-Type"]="application/json"
       
       
        return response2
    
        
    
@app.route('/bakeries/<int:id>',methods=["GET","PATCH","DELETE"])
def bakeries_id(id):
    single_bakery=Bakery.query.filter_by(id=id).first()

    if request.method=="GET":
        single_bakery_dict=single_bakery.to_dict()
        response1=make_response(jsonify(single_bakery_dict),200)
        response1.headers["Content-Type"]="application/json"
        
        
        return response1
    

    elif request.method=="PATCH":
        for attribute in request.form:
            setattr(single_bakery,attribute,request.form.get(attribute))
        db.session.commit()
        single_bakery_dict2=single_bakery.to_dict()
        response2=make_response(jsonify(single_bakery_dict2),200)
        response2.headers["Content-Type"]="application/json"
       
       
        return response2
    
    elif request.method=="DELETE":
        db.session.delete(single_bakery)
        db.session.commit()

        response_body = {
                "delete_successful": True,
                "message": "Review deleted."
            }
        response3=make_response(jsonify(response_body),200)
        response3.headers["Content-Type"]="application/json"
        
        
        return response3



if __name__ == '__main__':
    app.run(port=5555, debug=True)
