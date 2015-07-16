import datetime

from app import db
from app.problem.models import Problem
from app.user_score.models import UserScore


class Contest(db.Model):

    __tablename__ = 'contests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    result_announced_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    problems = db.relationship(Problem, backref='contest', lazy='dynamic')
    scores = db.relationship(UserScore, backref='contest', lazy='dynamic')

    def submissions_count(self):
        return sum(map(len, [problem.submissions.all() for problem in self.problems]))

    def is_ended(self):
        return datetime.datetime.now() > self.end_at

    def is_started(self):
        return datetime.datetime.now() > self.start_at

    def __str__(self):
        return self.name

    def is_running(self):
        return self.is_started() and not self.is_ended()
