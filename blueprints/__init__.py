import config
import json
import os

from functools import wraps
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_claims, verify_jwt_in_request
from flask import Flask, request, send_from_directory
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

###############################################################
app = Flask(__name__)

my_flask = os.environ.get('FLASK_ENV', 'Production')
if my_flask == 'Production':
    app.config.from_object(config.ProductionConfig)
elif my_flask == 'Testing':
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    ## dipake jadi trycatch soalnya response iamge ga bisa di decode json
    try : 
        if response.status_code == 200:
            app.logger.info("REQUEST_LOG\t%s",
                            json.dumps({
                                'status_code': response.status_code,
                                'method': request.method,
                                'code': response.status,
                                'uri': request.full_path,
                                'request': requestData,
                                'response': json.loads(response.data.decode('utf-8'))
                            })
                            )
        else:
            app.logger.error("REQUEST_LOG\t%s",
                            json.dumps({
                                'status_code': response.status_code,
                                'method': request.method,
                                'code': response.status,
                                'uri': request.full_path,
                                'request': requestData,
                                'response': json.loads(response.data.decode('utf-8'))
                            })
                            )
    except Exception as e:
        pass
    return response


# Import Blueprint
from blueprints.user.resources import bp_user
from blueprints.personal_messages.resources import bp_personal_message

# Register Blueprint
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_personal_message, url_prefix='/pm')

db.create_all()
