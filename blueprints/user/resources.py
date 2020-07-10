from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims
import json
from .model import Users
from blueprints import db, app
from sqlalchemy import desc

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class User(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('phone_number', location='json', required=True)
        args = parser.parse_args()


        user = Users(args['name'], args['phone_number'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}

    def get(self, id):
        user = Users.query.get(id)
        app.logger.debug('DEBUG : %s', user)
        return marshal(user, Users.response_fields), 200

    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        parser.add_argument('phone_number', location='json')
        args = parser.parse_args()

        user = Users.query.get(id)
        if args['name'] is not None:
            user.name = args['name']
        if args['phone_number'] is not None:
            user.phone_number = args['phone_number']
        
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)
        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}

api.add_resource(User, '', '/<id>')
