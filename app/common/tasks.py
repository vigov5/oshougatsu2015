import os
import time
import json

from celery.utils.log import get_task_logger

from app import app, db, celery
from app.common.utils import generate_random_string
from app.common import constants as COMMON
from app.submission.models import Submission
from app.submission import constants as SUBMISSION


logger = get_task_logger(__name__)

@celery.task(name="tasks.run_code")
def run_code(problem_id, submission_id, source_name_with_prefix, target_name, language):
    try:
        run_folder = generate_random_string(7)
        temp_path = os.path.join(app.config['RUN_FOLDER'], run_folder)
        testcase_folder = os.path.join(app.config['TESTCASE_FOLDER'], str(problem_id))
        submission_source = os.path.join(app.config['SUBMISSION_FOLDER'], source_name_with_prefix)
        submission_target = os.path.join(temp_path, target_name)

        # copy payload folder to temp folder
        os.system("cp -R %s %s" % (app.config['PAYLOAD_FOLDER'], temp_path))
        # copy testcase to temp folder
        os.system("cp -R %s %s" % (testcase_folder, os.path.join(temp_path, 'testcases')))
        # copy source code to temp folder
        os.system("cp %s %s" % (submission_source, submission_target))
        # chmod 777
        os.system("chmod 777 -R %s" % temp_path)

        cmd = "docker run -d -u mysql -i -t -v  '%s':/usercode virtual_machine /usercode/supervisor.py %s /usercode %s %s" % (temp_path, 2, language, target_name)
        logger.debug(cmd)
        os.system(cmd)
        count = 0
        result_file = os.path.join(temp_path, 'result')
        while count <= COMMON.TASK_TIMEOUT_SEC:
            if os.path.isfile(result_file):
                with open(result_file, 'r') as f:
                    data = json.loads(f.read())
                    logger.debug(data)
                    submission = Submission.query.get(int(submission_id))
                    submission.state = SUBMISSION.STATE_FINISHED
                    if data['success']:
                        submission.used_time = data['time']
                        submission.used_memory = data['memory']
                    elif data['reason'] == SUBMISSION.RESULT_WRONG_ANSWER:
                        submission.failed_test_case_result = data['failed_test_case_result']
                    submission.last_passed_test_case = data['last_passed_test_case']
                    submission.result_status = data['reason']
                    db.session.add(submission)
                    db.session.commit()
                    break
            time.sleep(1)
            count += 1
    except Exception, e:
        print e
    finally:
        os.system("rm -rf %s" % temp_path)
