from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class RunsModel(db.Model):
    __tablename__ = 'trips_runs'

    index = db.Column(db.Integer, primary_key=True, nullable=False)
    IN = db.Column(db.Integer)
    Run_id = db.Column(db.Float)

    def __init__(self, in_count, run_id):
        self.IN = in_count
        self.Run_id = run_id

    def __repr__(self):
        return f'{self.Run_id}: {self.IN}'






