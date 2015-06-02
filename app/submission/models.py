import datetime

from app import db


class Submission(db.Model):

    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    language = db.Column(db.Integer)
    state = db.Column(db.String(255))
    result_status = db.Column(db.String(255))
    last_passed_test_case = db.Column(db.Integer)
    used_time = db.Column(db.Integer)
    used_memory = db.Column(db.Integer)
    received_point = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    failed_test_case_result = db.Column(db.String(255))
