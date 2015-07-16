import os
import datetime

from app import app, db
from app.submission import constants as SUBMISSION


class Submission(db.Model):

    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    language = db.Column(db.Integer)
    state = db.Column(db.String(255))
    result_status = db.Column(db.String(255), default='')
    last_passed_test_case = db.Column(db.Integer, default=0)
    used_time = db.Column(db.Integer, default=0)
    used_memory = db.Column(db.Integer, default=0)
    received_point = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    failed_test_case_result = db.Column(db.String(255))

    def __init__(self, problem_id, user_id, language):
        self.user_id = user_id
        self.problem_id = problem_id
        self.language = language

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

    def get_source_name(self):
        return str(self.id) + '.' + SUBMISSION.LANG_EXTENSIONS[self.language]

    def get_target_name(self):
        if self.language == SUBMISSION.LANG_JAVA:
            return 'Main.java'
        else:
            return self.get_source_name()

    def get_source_name_with_prefix(self):
        return os.path.join(
            self.get_source_prefix(),
            self.get_source_name()
        )

    def get_target_name_with_prefix(self):
        return os.path.join(
            self.get_source_prefix(),
            self.get_target_name()
        )

    def get_source_prefix(self):
        return os.path.join(
            str(self.user_id),
            str(self.problem_id),
            str(self.id)
        )

    def save_source_code(self, source_code):
        try:
            source_code_folder = os.path.join(app.config['SUBMISSION_FOLDER'], self.get_source_prefix())
            os.system("mkdir -p %s" % source_code_folder)
            f = open(os.path.join(source_code_folder, self.get_source_name()), 'w')
            f.write(source_code.read())
            return True
        except Exception, e:
            print e
            return False

    def get_source_code(self):
        try:
            source_file_path = os.path.join(app.config['SUBMISSION_FOLDER'], self.get_source_name_with_prefix())
            with open(source_file_path, 'r') as f:
                return f.read()
        except Exception, e:
            return ''

    def get_language_mapping(self):
        return SUBMISSION.LANG_PARAMS_MAPPING[self.language]

    def get_language_name(self):
        return SUBMISSION.LANGUAGES[self.language]

    def update_receive_point(self):
        if self.problem.contest.is_running():
            if self.problem.submissions.filter_by(user_id=self.user_id, result_status=SUBMISSION.RESULT_ACCEPTED).count() != 0:
                self.received_point = 0
            else:
                fail_submissions = self.problem.submissions. \
                    filter_by(user_id=self.user_id, state=SUBMISSION.STATE_FINISHED). \
                    filter(Submission.result_status != SUBMISSION.RESULT_ACCEPTED)
                wrong_points = fail_submissions.count() * self.problem.wrong_answer_decreased_point

                diff = datetime.datetime.now() - self.problem.contest.start_at
                interval_points = int(diff.total_seconds() / self.problem.slowly_decreased_interval)

                if self.problem.starting_point > wrong_points + interval_points:
                    self.received_point = self.problem.starting_point - wrong_points - interval_points
                else:
                    self.received_point = 0
        else:
            self.received_point = 0
