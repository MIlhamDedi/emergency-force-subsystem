from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
from flask_login import LoginManager, login_user, logout_user, \
    login_required
from subsystem.data_model import Asset, Plan, Report, User
from subsystem.config import SECRET_KEY
from psycopg2 import OperationalError
from werkzeug.security import check_password_hash, generate_password_hash

database_working = True
try:
    from subsystem.database_interface import get_asset, get_plan, get_report, \
        get_users, add_users
    asset_data = Asset(get_asset())
    plan_data = Plan(get_plan())
    report_data = Report(get_report())
    user_data = dict()
    for _ in get_users():
        user_data[_[0]] = _[1]
except OperationalError:
    database_working = False
app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = SECRET_KEY


# User Handler
@login_manager.user_loader
def load_user(user_id):
    if user_id in user_data:
        return User(user_id)
    else:
        return None


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


# Login/Signup Function
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = "Please, login into your account"
    if request.method == 'POST':
        uid = request.form.get('username')
        pwd = request.form.get('password')
        user = User(uid)
        if uid in user_data:
            if check_password_hash(user_data[uid], pwd):
                user.set_authenticated(True)
                if login_user(user):
                    return redirect(url_for('index'))
            else:
                error = "Wrong Username or Password"
    return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        print("yay post")
        uid = request.form.get('username')
        pwd = request.form.get('password')
        pwd_hashed = generate_password_hash(pwd)
        del pwd
        add_status = add_users(uid, pwd_hashed, 'user')
        if add_status == 1:
            error = "Username already taken"
            print("fail")
        else:
            user_data[uid] = pwd_hashed
            return redirect(url_for('login'))
    return render_template('signup.html', error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Dashboard Website
@app.route('/')
@login_required
def index():
    global asset_data, plan_data, report_data
    return (render_template(
        'index.html',
        asset=asset_data.json,
        plan=plan_data.json,
        report=report_data.json) if database_working else render_template(
            'index.html', asset_data={}, plan={}, report={}, users=None))


# API
class asset_api(Resource):
    def get(self):
        return asset_data.json if database_working else {}


class report_api(Resource):
    def get(self):
        return report_data.json if database_working else {}


class plan_api(Resource):
    def get(self):
        return plan_data.json if database_working else {}


api.add_resource(asset_api, '/asset/api')
api.add_resource(report_api, '/report/api')
api.add_resource(plan_api, '/plan/api')
