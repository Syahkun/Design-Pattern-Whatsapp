from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims
import json
from .model import PersonalMessages
from blueprints.conversation.model import Conversations
from blueprints.user.model import Users
from blueprints import db, app
from sqlalchemy import desc

bp_personal_message = Blueprint('personal_message', __name__)
api = Api(bp_personal_message)

class PersonalMessageResource(Resource):

    def get(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('userB_id', location='args', required=True)
        args = parser.parse_args()
        # qry=

    
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('userB_id', location='args', required=True)
        parser.add_argument('message', location='args')
        args = parser.parse_args()
        
        if args['userB_id'] == Users.query.get(id).id:
            app.logger.debug('DEBUG: Cannot send to self')
            return {'status': 'error send message'}, 403
        
        conversation = Conversations.query.filter_by(userA_id=Users.query.get(id).id)
        conversation = conversation.filter_by(userB_id=args['userB_id']).first()
        
        if conversation is None:
            conversation = Conversations.query.filter_by(userB_id=Users.query.get(id).id)
            conversation = conversation.filter_by(userA_id=args['userB_id']).first()
        
            if conversation is None:
                conversation = Conversations(Users.query.get(id).id, args['userB_id'])
                db.session.add(conversation)
                db.session.commit()        
        
        personal_message = PersonalMessages(Users.query.get(id).id, conversation.id, args['message'])
        db.session.add(personal_message)
        db.session.commit()
        
        app.logger.debug('DEBUG: success')
        return marshal(personal_message, PersonalMessages.response_fields), 200

    def delete(self, id):
        personal_message = PersonalMessages.query.get(id)
        if personal_message is None:
            app.logger.debug("DEBUG: ID not found")
            return {'status':"NOT_FOUND"}, 404
        
        db.session.delete(personal_message)
        db.session.commit()
        
        app.logger.debug("DEBUG: Data Deleted")
        return {'status':'Success deleted'}, 200
    
api.add_resource(PersonalMessageResource, '', '/<id>')