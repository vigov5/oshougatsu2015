from flask import g, Blueprint, request
from flask import jsonify
from flask_cors import CORS, cross_origin

from app import db
from app.problem.models import Problem
from app.user.models import User
from app.submission.models import Submission
from app.submission import constants as SUBMISSION


api_v1_module = Blueprint('api_v1', __name__)

@api_v1_module.route('/problem/<int:problem_id>', methods=['GET'])
def problem(problem_id=None):
    respose = {'success': False, 'result': False}
    try:
        problem = Problem.query.get(problem_id)
        user = User.query.filter_by(email=request.args.get('email', '')).all()
        if problem and user:
            submissions = problem.submissions.filter_by(user_id=user[0].id, result_status=SUBMISSION.RESULT_ACCEPTED).all()
            if len(submissions):
                respose['result'] = True
                respose['point'] = max([submission.received_point for submission in submissions])
        
        respose['success'] = True

        return jsonify(respose)
    except Exception, e:
        print e
        return jsonify(respose)


@cross_origin()
@api_v1_module.route('/game', methods=['GET'])
def game():
    problem_id = request.args.get('id', 0)
    email = request.args.get('email', '')
    email = email.replace('"', '')
    user = User.query.filter_by(email=email).first()
    problem = Problem.query.get(problem_id)
    if not user or not problem_id:
        return jsonify(respose = {'success': False, 'result': False})

    submission = Submission(problem_id, user.id, 0)
    submission.state = SUBMISSION.STATE_FINISHED
    submission.result_status = SUBMISSION.RESULT_ACCEPTED
    submission.received_point = problem.starting_point
    db.session.add(submission)
    db.session.commit()

    return jsonify(respose = {'success': True, 'result': True})
