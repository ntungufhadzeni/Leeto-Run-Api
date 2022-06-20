#!/usr/bin/python3
import json

from flask import Flask, request, make_response
from marshmallow import fields
from flask_marshmallow import Marshmallow
from sqlalchemy import and_
from flask_migrate import Migrate
from models import db, RunsModel
from datetime import datetime

with open('credentials.json', 'r') as fileObj:
    data = json.load(fileObj)

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{data['USER']}:{data['PASSWORD']}@{data['HOST']}:{data['PORT']}/{data['DBNAME']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


class TripsSchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = RunsModel
        sqla_session = db.session

    bus = fields.Integer()
    run = fields.String()
    date = fields.String()
    route = fields.String()


class StopsSchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = RunsModel
        sqla_session = db.session

    In = fields.Integer()
    Out = fields.Integer()
    route = fields.String()
    run = fields.String()
    date = fields.String()
    stop_name = fields.String()
    alarm = fields.String()


@app.route('/runs', methods=['GET'])
def get_total_by_id():
    args = request.args
    name = args.get('run')
    date = args.get('date')
    total = 0

    name_list = name.split()
    route = name_list[0]
    run = name_list[1]

    if run.find(':') != -1:
        run_list = run.split(':')
        run = 'H'.join(run_list)

    result = RunsModel.query.filter(
        and_(RunsModel.run == run, RunsModel.alarm.startswith(date), RunsModel.route.startswith(route)))

    result_schema = TripsSchema()
    result_schema_all = StopsSchema()
    result_all = result.all()
    for i in range(len(result_all)):
        result_dict = result_schema_all.dump(result_all[i])
        if result_dict['stop_name'] == "Church Street":
            continue
        total = total + result_dict['In']
    dict_result = result_schema.dump(result.first())
    bus = dict_result['bus']
    if bus < 10:
        bus = '00' + str(bus)
    else:
        bus = '0' + str(bus)

    dict_result['bus'] = bus
    dict_result.setdefault('total', total)

    return make_response(dict_result)


@app.route('/trips', methods=['GET'])
def get_stops_in():
    args = request.args
    name = args.get('run')
    date = args.get('date')
    name_list = name.split()
    route = name_list[0]
    run = name_list[1]
    result_dict = {}

    if run.find(':') != -1:
        run_list = run.split(':')
        run = 'H'.join(run_list)

    result = RunsModel.query.filter(
        and_(RunsModel.run == run, RunsModel.alarm.startswith(date), RunsModel.route.startswith(route))).all()
    result_schema = StopsSchema()

    for i in range(len(result)):
        dict_result = result_schema.dump(result[i])
        stop = dict_result['stop_name']
        if stop == "Church Street":
            continue
        in_count = dict_result['In']
        result_dict.setdefault(stop, in_count)
    return make_response(result_dict)


if __name__ == '__main__':
    app.run(debug=True)
