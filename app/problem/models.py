import datetime

from app import db
from app.problem import constants as PROBLEM


class Problem(db.Model):

    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey('contests.id'))
    name_vi = db.Column(db.String(255))
    name_en = db.Column(db.String(255))
    content_vi = db.Column(db.Text)
    content_en = db.Column(db.Text)
    rank = db.Column(db.Integer)
    limited_time = db.Column(db.Integer)
    limited_memory = db.Column(db.Integer)
    limited_source_size = db.Column(db.Integer)
    starting_point = db.Column(db.Integer)
    wrong_answer_decreased_point = db.Column(db.Integer)
    slowly_decreased_interval = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    submissions = db.relationship('Submission', backref='problem', lazy='dynamic')

    def get_rank_text(self):
        return PROBLEM.RANKS[self.rank]

    def get_name(self, user):
        if user and user.is_authenticated():
            return self.name_vi if user.is_locale_vn() else self.name_en
        else:
            return self.name_en
