import os
import datetime

from app import app, db


class Hint(db.Model):
    __tablename__ = 'hints'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    is_open = db.Column(db.Boolean)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))

    def __repr__(self):
        return '<Hint %r>' % (self.description)

    def __init__(self, description='', is_open=False, problem=None):
        self.description = description
        self.is_open = is_open
        self.problem = problem