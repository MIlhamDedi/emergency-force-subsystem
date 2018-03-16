from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
from .database_interface import connect, get_asset, get_plan, get_report
HOSTNAME = ""
PORT = ""
DB_NAME = ""
UID = ""
PWD = ""
app = Flask(__name__)
api = Api(app)

connect(HOSTNAME, PORT, DB_NAME, UID, PWD)
asset_data = get_asset()
plan_data = get_plan()
report_data = get_report()


# WebPage
@app.route('/')
def index():
    global asset_data, plan_data, report_data
    return render_template(
        'index.html', asset=asset_data, plan=plan_data, report=report_data)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/plan/')
def plan_page():
    return render_template('plan.html')


@app.route('/report/')
def report_page():
    return render_template('report.html')


@app.route('/asset/')
def asset_page():
    return render_template('asset.html')


# API
class asset_api(Resource):
    def get(self):
        global asset_data
        return asset_data


class report_api(Resource):
    def get(self):
        global report_data
        return report_data


class plan_api(Resource):
    def get(self):
        global plan_data
        return plan_data


api.add_resource(asset_api, '/api/asset')
api.add_resource(report_api, '/api/report')
api.add_resource(plan_api, '/api/plan')

if __name__ == '__main__':
    app.run(debug=True)
