import os
from flask import Flask, render_template, jsonify, request, Blueprint, send_from_directory
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_jwt_extended import(
    JWTManager, get_jwt_identity
)
from models import db, Consumer, Category, Bottle, Exchage
from routes.authconsumer import authconsumer
from routes.image import images

from werkzeug.utils import secure_filename #move to new route file
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static')

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JWT_SECRET_KEY'] = 'super-secrets'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1000)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'fineukraine94@gmail.com'
app.config['MAIL_PASSWORD'] = 'dqhxchlvckgjlbks'
jwt = JWTManager(app)
db.init_app(app)
mail = Mail(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html', name = 'home')

app.register_blueprint(authconsumer)
app.register_blueprint(images)

if __name__ == '__main__':
    manager.run()