"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
import json

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['ENV'] = 'development'
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson" )

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

""" @app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
        
    }


    return jsonify(response_body), 200 """

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    if not members:
        return jsonify({"msg" "bad request"}), 400
    else:
        response_body = {
            "family": members
            }

    return jsonify({"msg": " success"}, response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"msg": "bad request"}), 400
    else:
        return jsonify({"msg": "success"}, member), 200

@app.route('/member', methods=['POST'])
def createMember():
    if not request.json.get('first_name'):
        return jsonify({"msg": "fisrt name is required"}), 404
    if not request.json.get('age'):
        return jsonify({"msg": "age is required"}), 404
    if not request.json.get('lucky_numbers'):
        return jsonify({"msg": "lucky numbers is required"}), 404

    jackson_family.first_name = request.json.get('first_name')
    jackson_family.age = request.json.get('age')
    jackson_family.lucky_numbers = request.json.get('lucky_numbers')

    jackson_family.add_member(jackson_family)
    return jsonify({"msg": "ok"}), 200
    


@app.route('/member/<int:id>', methods=['DELETE'])
def deleteSingleMember(id):
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"msg": "bad request"}), 400
    else:
        jackson_family.delete_member(id)
        return jsonify({"msg": "done"}, member), 200
       
@app.route('/member/<int:id>', methods=['PUT'])
def update(id):
    member = jackson_family.get_member(id)
    
    first_name = request.json.get('first_name')
    age = request.json.get('age')
    lucky_numbers = request.json.get('lucky_numbers')

    if not first_name:
        return jsonify({"msg": "first anme is required"}), 400
    if not age:
        return jsonify({"msg": "age is required"}), 400
    if not lucky_numbers:
        return jsonify({"msg": "lucky numbers is required"}), 400

    member["first_name"] = first_name
    member["age"] = age
    member["lucky_numbers"] = lucky_numbers

    return jsonify({"success": "member has been edited"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
