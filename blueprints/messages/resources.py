from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims
from blueprints import db, app
from sqlalchemy import desc, or_
from datetime import datetime
from flask import Blueprint
# import moment
# import humanize

from blueprints.conversation.model import Conversations
from blueprints.personal_message.model import PersonalMessages
from blueprints.user.model import Users


bp_message = Blueprint('message', __name__)
api = Api(bp_message)

class MessageResource(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='args', required=True)
        args = parser.parse_args()

        list_chat = []

        # ambil data personal chat
        conversations = Conversations.query.filter(or_(Conversations.userA_id.like(args['user_id']), Conversations.userB_id.like(args['user_id'])))
        for conversation in conversations:
            marshal_conversation = marshal(
                conversation, Conversations.response_fields)

            # memasukkan data lawan chat
            if marshal_conversation['userA_id'] != args['user_id']:
                user = Users.query.get(marshal_conversation['userA_id'])
                marshal_user = marshal(user, Users.response_fields)
                marshal_conversation['info_chat'] = marshal_user
            # memasukkan data lawan chat
            if marshal_conversation['userB_id'] != args['user_id']:
                user = Users.query.get(marshal_conversation['userB_id'])
                marshal_user = marshal(user, Users.response_fields)
                marshal_conversation['info_chat'] = marshal_user

            # filter chat by user yang login
            personal_messages = PersonalMessages.query.filter_by(
                conversation_id=conversation.id)

            # mengambil data pesan terakhir
            last_personal_messages = personal_messages.order_by(desc(PersonalMessages.created_at)).first()
            marshal_last_personal_messages = marshal(last_personal_messages, PersonalMessages.response_fields)
            marshal_conversation['last_chat'] = marshal_last_personal_messages

            # mengambil semua chat
            list_message = []
            for personal_message in personal_messages:
                marshal_personal_message = marshal(
                    personal_message, PersonalMessages.response_fields)
                list_message.append(marshal_personal_message)

                # memasukkan data user yang mengirim chat selain user yang sedang login
                if marshal_personal_message['user_id'] == marshal_conversation['info_chat']['id']:
                    user = Users.query.get(
                        marshal_conversation['info_chat']['id'])
                    marshal_user = marshal(user, Users.response_fields)
                    marshal_personal_message['user'] = marshal_user

            marshal_conversation['all_chat'] = list_message

            list_chat.append(marshal_conversation)
            personal_messages = PersonalMessages.query.filter_by(
                conversation_id=conversation.id)

            # mengambil data pesan terakhir
            last_personal_messages = personal_messages.order_by(desc(PersonalMessages.created_at)).first()
            marshal_last_personal_messages = marshal(last_personal_messages, PersonalMessages.response_fields)
            marshal_conversation['last_chat'] = marshal_last_personal_messages

            # mengambil semua chat
            list_message = []
            for personal_message in personal_messages:
                marshal_personal_message = marshal(
                    personal_message, PersonalMessages.response_fields)
                list_message.append(marshal_personal_message)

                # memasukkan data user yang mengirim chat selain user yang sedang login
                if marshal_personal_message['user_id'] == marshal_conversation['info_chat']['id']:
                    user = Users.query.get(
                        marshal_conversation['info_chat']['id'])
                    marshal_user = marshal(user, Users.response_fields)
                    marshal_personal_message['user'] = marshal_user

            marshal_conversation['all_chat'] = list_message

            list_chat.append(marshal_conversation)
        return list_chat, 200

api.add_resource(MessageResource, '', '')