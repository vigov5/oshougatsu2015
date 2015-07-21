from flask import g, Blueprint, request
from flask import jsonify

from app import db
from app.problem.models import Problem
from app.user.models import User
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
