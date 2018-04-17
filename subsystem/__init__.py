from flask import Flask, render_template, request, redirect, url_for
from flask_restplus import Resource, Api
from flask_login import LoginManager, login_user, logout_user,\
    login_required, current_user
from subsystem.data_model import db, Asset, Plan, Report, User
from subsystem.config import SECRET_KEY, POSTGRES_URI
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import DataError
from uuid import uuid4

app = Flask(__name__)
api = Api(app, doc='/api/')
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
@api.route('/api/asset')
class asset_api(Resource):
    def get(self):
        return {a: b for (a, b) in (i.convert() for i in Asset.query.all())}

    def post(self):
        print(request)
        try:
            newAsset = Asset(
                name=request.form['name'],
                availability=request.form['availability'])
            db.session.add(newAsset)
            db.session.commit()
            return {
                newAsset.id: {
                    "name": newAsset.name,
                    "availability": newAsset.availability
                }
            }
        except KeyError:
            return "Not Enough data", 400
        except DataError:
            return "Wrong Type of Data", 400


@api.route('/api/report')
class report_api(Resource):
    def get(self):
        return [a.convert() for a in Report.query.all()]

    def post(self):
        # TODO: Add change in asset here
        try:
            newReport = Report(
                crisis_id=request.form['crisis_id'],
                assets_used=request.form['assets_used'],
                casualty=request.form['casualty'],
                details=request.form['details'],
                time=request.form['time'])
            db.session.add(newReport)
            db.session.commit()
            return {
                newReport.id: {
                    "crisis_id": newReport.crisis_id,
                    "assets_used": newReport.assets_used_parsed,
                    "casualty": newReport.casualty_parsed,
                    "details": newReport.details,
                    "time": str(newReport.time)
                }
            }
        except KeyError:
            return "Not Enough Data", 400
        except DataError:
            return "Wrong Type of Data", 400


@api.route('/api/plan')
class plan_api(Resource):
    def get(self):
        return [a.convert() for a in Plan.query.all()]

    def post(self):
        try:
            newPlan = Plan(
                crisis_id=request.form['crisis_id'],
                details=request.form['details'],
                time=request.form['time'])
            db.session.add(newPlan)
            db.session.commit()
            return {
                newPlan.id: {
                    "crisis_id": newPlan.crisis_id,
                    "details": newPlan.details,
                    "time": str(newPlan.time)
                }
            }
        except KeyError:
            return "Not Enough data", 400
        except DataError:
            return "Wrong Type of Data", 400
