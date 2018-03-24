import os
import json
from flask import Flask, render_template, session, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import hashlib
from suds.client import Client
from xml.sax.saxutils import escape


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def gettext(username, password):
    url = 'http://114.55.172.147:9701/MemberService.asmx?wsdl'
    client = Client(url)
    m = hashlib.md5(password.encode('utf-8'))
    pswd = m.hexdigest()
    print(username)
    print(pswd)
    text=client.service.MemberLoginJson(sCondition=username, sPassword=pswd)
    dic = json.loads(escape(text))
    return dic

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


'''
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    passowrd = db.Column(db.String(64),)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username
'''

class Info(db.Model):
    __tablename__ = 'Info'
    id = db.Column(db.Integer, primary_key=True)
    contacts = db.Column(db.String(64), unique=True)
    def __repr__(self):
        return '<Info> %r>' % self.contacts


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('帐号', validators=[DataRequired()])
    password = StringField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')
   
def log(name,pswd) -> None:
    with open('vsearch.log', 'a') as log:
        print(name,pswd,file=log)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/status', methods=['GET', 'POST'])
def hotel():
    username = request.form['username']
    password = request.form['password']
    x = gettext(username,password)
    if isinstance(x, dict):
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
