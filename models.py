from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class RunsModel(db.Model):
    __tablename__ = 'trips_v2'

    id = db.Column('index', db.Integer, primary_key=True, nullable=False)
    run = db.Column('Run', db.String)
    alarm = db.Column('Alarm Time', db.String)
    bus = db.Column('Bus No', db.Float)
    route = db.Column('Route', db.String)
    date = db.Column('Date', db.String)
    stop_name = db.Column('Stop Name', db.String)
    In = db.Column('IN', db.Integer(), nullable=False)
    Out = db.Column('Out', db.Integer(), nullable=False)







