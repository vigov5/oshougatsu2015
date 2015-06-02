import datetime

from app import db
from app.submission import constants as SUBMISSION


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

    def is_queued(self):
        return self.state == SUBMISSION.STATE_QUEUED

    def is_finished(self):
        return self.state == SUBMISSION.STATE_FINISHED

    def is_time_exceeded(self):
        return self.result_status == SUBMISSION.RESULT_TIME_EXCEEDED

    def is_memory_exceeded(self):
        return self.result_status == SUBMISSION.RESULT_MEMORY_EXCEEDED

    def is_compile_error(self):
        return self.result_status == SUBMISSION.RESULT_COMPILE_ERROR

    def is_runtime_error(self):
        return self.result_status == SUBMISSION.RESULT_RUNTIME_ERROR

    def is_wrong_answer(self):
        return self.result_status == SUBMISSION.RESULT_WRONG_ANSWER

    def is_accepted(self):
        return self.result_status == SUBMISSION.RESULT_ACCEPTED
