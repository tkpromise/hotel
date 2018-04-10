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
	
def getintegral(username, password):
    url = 'http://114.55.172.147:9701/MemberService.asmx?wsdl'
    client = Client(url)
    m = hashlib.md5(password.encode('utf-8'))
    pswd = m.hexdigest()
    text=client.service.MemberLoginJson(sCondition=username, sPassword=pswd)
    dic = json.loads(escape(text))
    mid = dic['MebID']
    integeral = client.service.GetMemberPointSum(nMebID=mid)
    return integeral

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
    jifen = getintegral(username, password)
    session['username'] = request.form['username']
    '''
    if isinstance(x, dict):
        return redirect('/my') 
    '''
    return render_template('my.html', the_in=jifen, username=username)

@app.route('/my', methods=['GET', 'POST'])
def my():
	return render_template('my.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/phonecase')
def phonecase():
	return render_template('phonecase.html')

@app.route('/towel')
def towel():
	return render_template('towel.html')

@app.route('/barbecue')
def barbecue():
	return render_template('barbecue.html')

@app.route('/b')
def b():
	return render_template('b.html')


@app.route('/qh78')
def qh78():
	return render_template('qh78.html')

@app.route('/ss161')
def ss161():
	return render_template('ss161.html')

@app.route('/sy688')
def sy688():
	return render_template('sy688.html')

@app.route('/sb2085')
def sb2086():
	return render_template('sb2085.html')


@app.route('/convert')
def convert():
	return render_template('convert.html')

@app.route('/search4', methods=['POST'])
def do_search() -> str:
	name = request.form['name']
	phone = request.form['phone']
	address = request.form['address']
	log_request(name, phone, address)
	return str('兑换成功')

def log_request(name, phone, address):
	with open('vsearch.log', 'a') as log:
		print(name, phone, address, file=log)

@app.route('/classification')
def classification():
	return render_template('classification.html')
