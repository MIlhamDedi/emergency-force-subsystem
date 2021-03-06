from flask import Flask, render_template, request, redirect, url_for
from flask_restplus import Resource, Api
from flask_login import LoginManager, login_user, logout_user,\
    login_required, current_user
from subsystem.data_model import db, Asset, Plan, Report, User
from subsystem.config import SECRET_KEY, POSTGRES_URI, CMO_URL
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import DataError, IntegrityError
from uuid import uuid4
import requests

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


########################
#     Login/Signup     #
########################
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    error = "false"
    if request.method == 'POST':
        uid = request.form.get('username')
        pwd = request.form.get('password')
        user = User.query.filter_by(username=uid).first()
        if user is None or not user.check_password(pwd):
            error = "true"
        else:
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = "false"
    if request.method == 'POST':
        uid = request.form.get('username')
        pwd = request.form.get('password')
        pwd_hashed = generate_password_hash(pwd)
        del pwd
        if User.query.filter_by(username=uid).first():
            error = "true"
        else:
            newUser = User(
                username=uid, pwd_hash=pwd_hashed, api_token=str(uuid4()))
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html', error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


####################
#     Webpages     #
####################
@app.route('/')
@login_required
def index():
    return (render_template('index.html', user=current_user.username))


#########################
#     Error Handler     #
#########################
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('error404'))


@app.route('/404')
@login_required
def error404():
    return (render_template('404.html', user=current_user.username))


###############
#     API     #
###############
api = Api(app, doc='/api/')


@api.route('/api/asset')
class asset_api(Resource):
    def get(self):
        return {
            a: b
            for (a, b) in (i.convert()
                           for i in Asset.query.order_by(Asset.id).all())
        }

    def post(self):
        try:
            newAsset = Asset(
                name=request.form['name'],
                availability=request.form['availability'])
            db.session.add(newAsset)
            db.session.commit()
            return {
                'error': "",
                'asset': {
                    'id': newAsset.id,
                    'name': newAsset.name,
                    'availability': newAsset.availability
                }
            }, 201
        except KeyError:
            return {'error': "Not Enough Data"}, 400
        except DataError:
            return {'error': "Wrong Type of Data"}, 400
        except IntegrityError:
            return {'error': "Asset with such name already exist"}, 403


@api.route('/api/asset/<int:asset_id>')
class asset_update_api(Resource):
    def get(self, asset_id):
        asset_data = Asset.query.filter_by(id=asset_id).first()
        if asset_data is None:
            return {"error": "No asset with that id"}, 400
        a = asset_data.convert()
        return {a[0]: a[1]}

    def post(self, asset_id):
        try:
            a = Asset.query.filter_by(id=asset_id).first()
            a.availability -= int(request.form['add'])
            db.session.commit()
            return {'error': ""}, 200
        except KeyError:
            return {'error': "Not Enough Data"}, 400
        except (DataError, ValueError, TypeError, AttributeError):
            return {'error': "Wrong Type of Data"}, 403


@api.route('/api/report')
class report_api(Resource):
    def get(self):
        return [
            a.convert() for a in Report.query.order_by(Report.id.desc()).all()
        ]

    def post(self):
        try:
            is_final_data = True if request.form[
                'is_final'].lower() == "true" else False
            newReport = Report(
                crisis_id=request.form['crisis_id'],
                assets_used=request.form['assets_used'],
                casualty=request.form['casualty'],
                details=request.form['details'],
                is_final=is_final_data,
                time=request.form['time'])
            db.session.add(newReport)
            db.session.commit()
            return {'error': '', 'report': newReport.convert()}, 201
        except KeyError:
            return {'error': "Not Enough Data"}, 400
        except DataError:
            return {'error': "Wrong Type of Data"}, 400


@api.route('/api/plan')
class plan_api(Resource):
    def get(self):
        return [a.convert() for a in Plan.query.order_by(Plan.id.desc()).all()]

    def post(self):
        try:
            newPlan = Plan(
                id=request.form['id'],
                crisis_id=request.form['crisis_id'],
                details=request.form['details'],
                time=request.form['time'])
            db.session.add(newPlan)
            db.session.commit()
            return {'error': "", 'plan': newPlan.convert()}, 201
        except KeyError:
            return {'error': "Not Enough Data"}, 400
        except DataError:
            return {'error': "Wrong Type of Data"}, 400
        except IntegrityError:
            return {'error': "Duplicate value of Data"}, 403


@api.route('/api/cmo')
class fetch_plan(Resource):
    def get(self):
        r1 = requests.get(CMO_URL)
        cmo_plan_list = r1.json()
        ef_plan_id_list = [
            a.id for a in Plan.query.order_by(Plan.id.desc()).all()
        ]
        added_id = []
        for _ in cmo_plan_list:
            if _['solution_id'] not in ef_plan_id_list:
                try:
                    newPlan = Plan(
                        id=_['solution_id'],
                        crisis_id=_['crisis_id'],
                        details=_['detail'],
                        time=_['date_time_of_send'])
                    db.session.add(newPlan)
                    db.session.commit()
                    added_id.append(_['solution_id'])
                except KeyError:
                    return {
                        'error': f"Not Enough Data on id {_['solution_id']}"
                    }, 400
                except DataError:
                    return {
                        'error': f"Wrong Type of Data on id {_['solution_id']}"
                    }, 400
                except IntegrityError:
                    return {
                        'error':
                        f"Duplicate value of Data on id {_['solution_id']}"
                    }, 403
        return {'error': 'none', 'added_id': added_id}, 201


@api.route('/api/plan/<int:plan_id>')
class plan_update_api(Resource):
    def get(self, plan_id):
        plan_data = Plan.query.filter_by(id=plan_id).first()
        if plan_data is None:
            return {"error": "No Plan with that id"}, 400
        return plan_data.convert()

    def post(self, plan_id):
        try:
            plan_data = Plan.query.filter_by(id=plan_id).first()
            plan_data.progress = int(request.form['progress'])
            db.session.commit()
            return {'error': "", 'plan': plan_data.convert()}, 200
        except KeyError:
            return {'error': "Not Enough Data"}, 400
        except (DataError, ValueError, AttributeError):
            return {'error': "Wrong Type of Data"}, 400
        except IntegrityError:
            return {'error': "Plan doesn't exist"}, 400
