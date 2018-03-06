#! /usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)
# Sample Data
asset_data = [['Police', 20], ['Tank', 5], ['Heli', 2]]
plan_data = [
    ['2 Police', "2018/2/15 15:32"],
    ['14 Police, 1 Tank', "2018/2/27 12:30"],
    ['6 Police, 1 Heli', "2018/3/2 17:57"],
]
report_data = [
    ['Success', "2018/2/15"],
    ['Success, Died 1, Hurt 6', "2018/2/27"],
    ['Success, Hurt 2', "2018/3/2"]
]


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
def plan():
    return render_template('plan.html')


@app.route('/report/')
def report():
    return render_template('report.html')


@app.route('/asset/')
def assets():
    return render_template('asset.html')


# API
class asset_api(Resource):
    def get(self):
        global asset_data
        return dict(asset_data)


class report_api(Resource):
    def get(self):
        global report_data
        return dict(report_data)


class plan_api(Resource):
    def get(self):
        global plan_data
        return dict(plan_data)


api.add_resource(asset_api, '/api/asset')
api.add_resource(report_api, '/api/report')
api.add_resource(plan_api, '/api/plan')

if __name__ == '__main__':
    app.run(debug=True)
