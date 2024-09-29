import psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "BSdskjbgihdiy45435316KDHISGFIfytr7dsgfu"
DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='Victus',url='localhost',db='testdb')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

from letdeal import routes