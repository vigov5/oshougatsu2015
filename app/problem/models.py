import os
import datetime

from app import app, db
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
    hints = db.relationship('Hint', backref='problem', lazy='dynamic')

    def get_rank_text(self):
        return PROBLEM.RANKS[self.rank]

    def get_name(self, user):
        if user and user.is_authenticated():
            return self.name_vi if user.is_locale_vn() else self.name_en
        else:
            return self.name_en

    def get_testcase_nums(self):
        test_files = []
        testcase_path = os.path.join(app.config['TESTCASE_FOLDER'], str(self.id))
        for root, dirs, files in os.walk(testcase_path, topdown=False):
            for name in files:
                if 'test' in name:
                    test_files.append(name)

        return len(test_files)

    def get_content(self, user):
        if user and user.is_authenticated():
            return self.content_vi if user.is_locale_vn() else self.content_en
        else:
            return self.content_en

    def get_testcase(self, num=1):
        try:
            testcase_file_path = os.path.join(app.config['TESTCASE_FOLDER'], str(self.id), "test%03d.txt" % num)
            with open(testcase_file_path, 'r') as f:
                return f.read()
        except Exception, e:
            return ''

    def get_output(self, num=1):
        try:
            output_file_path = os.path.join(app.config['TESTCASE_FOLDER'], str(self.id), "out%03d.txt" % num)
            with open(output_file_path, 'r') as f:
                return f.read()
        except Exception, e:
            return ''

    def __str__(self):
        return self.name_en
