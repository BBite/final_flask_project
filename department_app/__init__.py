"""
Sources root package.

Initializes web application and web service, contains following subpackages and modules:

Subpackages:
- `forms`: contains modules with forms
- `migrations`: contains migration files used to manage database schema
- `models`: contains modules with Python classes describing database models
- `rest`: contains modules with RESTful service implementation
- `schemas`: contains modules with serialization/deserialization schemas for models
- `service`: contains modules with classes used to work with database
- `static`: contains web application static files (styles, images)
- `templates`: contains web application html templates
- `views`: contains modules with web controllers/views
- `tests`: contains modules with unit tests
"""

# pylint: disable=wrong-import-position

import os
import sys
import logging

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from flask_restful import Api

cur_dir = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = (cur_dir[:cur_dir.find('\\final_project') + len('\\final_project')]
            if cur_dir.find('\\final_project') != -1 else cur_dir)
TEMPLATES_DIR = 'templates'
MIGRATION_DIR = os.path.join('department_app', 'migrations')

app = Flask(__name__, template_folder=TEMPLATES_DIR)

# from dotenv import load_dotenv
#
# load_dotenv(os.path.join(BASE_DIR, '.env'))

app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db, directory=MIGRATION_DIR)

api = Api(app)

from department_app.views import init_blueprints

init_blueprints(app)

from department_app.rest import init_api

init_api(api)

# logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

file_handler = logging.FileHandler(filename=os.path.join(BASE_DIR, 'app.log'), mode='w')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

app.logger.handlers.clear()
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.DEBUG)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.handlers.clear()
werkzeug_logger.addHandler(file_handler)
werkzeug_logger.addHandler(console_handler)
werkzeug_logger.setLevel(logging.DEBUG)
