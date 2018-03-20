import sys
from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
from .data_model import Asset, Plan, Report
from psycopg2 import OperationalError
database_working = True
try:
    from .database_interface import get_asset, get_plan, get_report
    asset_data = Asset(get_asset())
    plan_data = Plan(get_plan())
    report_data = Report(get_report())
except OperationalError:
    database_working = False
app = Flask(__name__)
api = Api(app)


# WebPage
@app.route('/')
def index():
    global asset_data, plan_data, report_data
    return (
        render_template('index.html', asset=asset_data.json, plan=plan_data.json, report=report_data.json) if database_working
        else render_template('index.html', asset_data={}, plan={}, report={}))


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
        return asset_data.json if database_working else {}


class report_api(Resource):
    def get(self):
        return report_data.json if database_working else {}


class plan_api(Resource):
    def get(self):
        return plan_data.json if database_working else {}


api.add_resource(asset_api, '/api/asset')
api.add_resource(report_api, '/api/report')
api.add_resource(plan_api, '/api/plan')
