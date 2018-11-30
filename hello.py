import os
import json
import hashlib
from flask import Flask, render_template, session, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from suds.client import Client
from xml.sax.saxutils import escape


from getmebidbyphone import reMebid
from getcouponbymebid import reCoupon
from getmemberpointsum import repoint

#flask_login
from flask_login import LoginManager, login_required, current_user, login_user, logout_user, UserMixin


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

#flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ='login'

def gettext(username, password):
    url = 'http://114.55.172.147:9701/MemberService.asmx?wsdl'
    client = Client(url)
    m = hashlib.md5(password.encode('utf-8'))
    pswd = m.hexdigest()
    print(username)
    print(pswd)
    text=client.service.MemberLoginJson(sCondition=username, sPassword=pswd)
    dic = json.loads(escape(text))
    if isinstance(dic, dict):
        return dic
    else:
        return 'None'
	
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

class NameForm(FlaskForm):
    username = StringField('帐号', validators=[DataRequired()])
    password = StringField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

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
#flask_login
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username
    return user

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
    if type(x) != dict:
        return redirect(url_for('login'))
    else:
        user = User()
        user.id = username
        login_user(user)
        jifen = getintegral(username, password)
        return render_template('my.html', the_in=jifen, username=username)
    '''
    if isinstance(x, dict):
    else:
        return render_template('login.html')
    '''

@app.route('/my', methods=['GET', 'POST'])
@login_required
def my():
	return render_template('my.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    username = 'admin'
    password = 'limit168'
    form = NameForm()
    if form.validate_on_submit():
        if username != form.username.data or password != form.password.data:
            session['user'] = form.username.data
            session['pswd'] = form.username.data
            return redirect('404')
    return render_template('my.html', the_in='80')

@app.route('/phonecase')
def phonecase():
	return render_template('phonecase.html')

@app.route('/towel')
@login_required
def towel():
	return render_template('towel.html')

@app.route('/barbecue')
def barbecue():
	return render_template('comm/03.html')

@app.route('/headphone')
def headphone():
	return render_template('comm/headphone.html')


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
@login_required
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

@app.route('/comm')
def comm():
    return render_template('comm.html')

@app.route('/comm1')
def comm1():
    return render_template('comm/comm1.html')

@app.route('/comm2')
def comm2():
    return render_template('comm/comm2.html')

@app.route('/comm23')
def comm23():
    return render_template('comm/comm23.html')

@app.route('/comm24')
def comm24():
    return render_template('comm/comm24.html')

@app.route('/comm25')
def comm25():
    return render_template('comm/comm25.html')

@app.route('/comm26')
def comm26():
    return render_template('comm/comm26.html')

@app.route('/comm27')
def comm27():
    return render_template('comm/comm27.html')

@app.route('/comm28')
def comm28():
    return render_template('comm/comm28.html')

@app.route('/comm29')
def comm29():
    return render_template('comm/comm29.html')

@app.route('/comm3')
def comm3():
    return render_template('comm/comm3.html')

@app.route('/comm4')
def comm4():
    return render_template('comm/comm4.html')

@app.route('/comm5')
def comm5():
    return render_template('comm/comm5.html')

@app.route('/comm6')
def comm6():
    return render_template('comm/comm6.html')
@app.route('/comm67')
def comm67():
    return render_template('comm/comm67.html')
@app.route('/comm68')
def comm68():
    return render_template('comm/comm68.html')

@app.route('/comm7')
def comm7():
    return render_template('comm/comm7.html')

@app.route('/comm8')
def comm8():
    return render_template('comm/comm8.html')

@app.route('/comm9')
def comm9():
    return render_template('comm/comm9.html')
    
@app.route('/comm10')
def comm10():
    return render_template('comm/comm10.html')



@app.route('/remebid', methods=['POST'])
def remebid():
    phone = request.form['phone']
    mebid = reMebid(phone)
    coupon = reCoupon(mebid)
    point = repoint(mebid)
    return render_template('coupon.html', phone = phone, mebid=coupon, point=point)


@app.route('/entry')
def query():
    return render_template('entry.html')

@app.route('/user/<mebid>')
def user(mebid):
    coupon = reCoupon(mebid)
    return render_template('coupon.html',mebid=coupon)

env = app.jinja_env
def format_num(num):
    if num!=1:
        return int(num) + '元'
    else:
        return num+'张'
env.filters['format_num'] = format_num



@app.route('/tech')
def tech():
    return render_template('tech.html')

@app.route('/en')
def en():
    return render_template('en.html')
