#!/usr/bin/python3
import json

from flask import Flask, request, jsonify, make_response
from marshmallow import fields
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from models import db, RunsModel

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

    index = fields.Number(dump_only=True)
    IN = fields.Number()
    Run_id = fields.Float()


@app.route('/', methods=['GET'])
def get_total_by_id():
    args = request.args
    run_id = args.get('run-id')
    run_id = float(run_id)
    result = RunsModel.query.filter(RunsModel.Run_id == run_id).one_or_none()

    result_schema = TripsSchema()
    return make_response(jsonify(result_schema.dump(result)))


if __name__ == '__main__':
    app.run(debug=True)
