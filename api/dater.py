from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from model.daters import Dater 
from __init__ import db


dating_api = Blueprint('dating_api', __name__,
                   url_prefix='/api/daters')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(dating_api)

class DaterResource(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()

            name = body.get('name')
            uid = body.get('uid')
            gender = body.get('gender')
            age = body.get('age')
            interests = body.get('interests')
            
            ''' Avoid garbage in, error checking '''
            # validate name
            if not name or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            if not gender or len(gender) < 2:
                return {'message': f'Gender is missing, or is less than 2 characters'}, 400
            if age is None:
                return {'message': 'Age is missing'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            dater = Dater(name=name, 
                      gender=gender, age=age, interests=interests, uid=uid)
            dater.create()
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            # success returns json of user
            if dater:
                return jsonify(dater.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or name {name} is duplicate'}, 400

class DaterListResource(Resource):
        def get(self): # Read Method
            daters = Dater.query.all()    # read/extract all users from database
            json_ready = [dater.read() for dater in daters]
            return jsonify(json_ready)
        
class DeleteResource(Resource):
        def delete(self, id):
            dater = Dater.query.get(id)
            if dater:
                dater.delete()
                return {'message': f'User with ID {id} deleted'}, 200
            else:
                return {'message': f'User with ID {id} not found'}, 404

    

            
api.add_resource(DaterResource, '/create')
api.add_resource(DeleteResource, '/delete/<int:id>')
api.add_resource(DaterListResource, '/')

