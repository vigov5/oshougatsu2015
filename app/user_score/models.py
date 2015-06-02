import datetime

from app import db


class UserScore(db.Model):

    __tablename__ = 'user_scores'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    contest_id = db.Column(db.Integer, db.ForeignKey('contests.id'))
    point = db.Column(db.Integer)
