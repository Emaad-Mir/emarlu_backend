from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from model.daters import Dater 
from __init__ import db


dating_api = Blueprint('dating_api', __name__,
                   url_prefix='/api/daters')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(dating_api)

def match_points(dic1, dic2):
        points = 0
        user1_int = [x.strip() for x in dic1["interests"].split("and")]
        print(user1_int)
        user2_int = [x.strip() for x in dic2["interests"].split("and")]
        print(user2_int) 
        for inter in user1_int:
            for interest in user2_int:
                if inter == interest:
                    points+= 1
        return points

class Create(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemented
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

class Read(Resource):
        def get(self): # Read Method
            daters = Dater.query.all()    # read/extract all users from database
            json_ready = [dater.read() for dater in daters]
            return jsonify(json_ready)
        
class Update(Resource):
        def put(self):
            daters = Dater.query.all()    # read/extract all users from database
            json_ready = [dater.read() for dater in daters]  # prepare output in json
            return jsonify(json_ready)
        
class Delete(Resource):
        def delete(self, id):
            dater = Dater.query.get(id)
            if dater:
                dater.delete()
                return {'message': f'User with ID {id} deleted'}, 200
            else:
                return {'message': f'User with ID {id} not found'}, 404

class Match(Resource):              
     def get(self, id, threshold):
        dater = Dater.query.get(id)
        dates = []
        if(dater):
            all = Dater.query.all()
            for date in all:
                if date.id == dater.id:
                     continue
                else:
                    point = match_points(dater.read(), date.read())
                    if point >= threshold:
                        dates.append(date)
            return jsonify([dater.read() for dater in dates])
        else:
             return {'message': f'User with ID {id} not found'}, 404


    

            
api.add_resource(Create, '/create')
api.add_resource(Read, '/')
api.add_resource(Update, '/update')
api.add_resource(Delete, '/delete/<int:id>')
api.add_resource(Match, '/match/<int:id>/<int:threshold>')


