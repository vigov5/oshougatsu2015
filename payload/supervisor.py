#!/usr/bin/env python3

"""
Script to supervisor code that run testcase
Usage: supervisor.py timeout prefix language file_name
"""

import os
import sys
import subprocess
import re
import json
from subprocess import TimeoutExpired, PIPE


TIMEOUT = int(sys.argv[1])
PREFIX = sys.argv[2]
LANGUAGE = sys.argv[3]
FILE_NAME = sys.argv[4]

TESTCASE_FOLDER = os.path.join(PREFIX, 'testcases')
RESULT_FILE = os.path.join(PREFIX, 'result')
SOURCE_CODE_FILE = os.path.join(PREFIX, FILE_NAME)

RESULT_TIME_EXCEEDED = 'Limited time exceeded'
RESULT_MEMORY_EXCEEDED = 'Limited memory exceeded'
RESULT_COMPILE_ERROR = 'Compile Error'
RESULT_RUNTIME_ERROR = 'Runtime Error'
RESULT_WRONG_ANSWER = 'Wrong Answer'
RESULT_ACCEPTED = 'Accepted'
RESULT_UNKNOWN_LANGUAGE = 'Unknown language'

test_files = []
out_files = []

def write_result(result):
    with open(RESULT_FILE, 'w') as f:
        f.write(json.dumps(result))

for root, dirs, files in os.walk(TESTCASE_FOLDER, topdown=False):
    for name in files:
        if 'test' in name:
            test_files.append(name)
        elif 'out' in name:
            out_files.append(name)
    break

test_files.sort()
out_files.sort()

i = 0
result = {'success': False}
max_memory = 0
max_time = 0
for test_file in test_files:
    proc = subprocess.Popen(['/usercode/run_code.sh', SOURCE_CODE_FILE, LANGUAGE, os.path.join(TESTCASE_FOLDER, test_file), PREFIX], stdout=PIPE, stderr=PIPE)
    try:
        outs, errs = proc.communicate(timeout=TIMEOUT)
        outs = outs.decode('utf-8').strip()
        if '[ERROR]' in outs:
            if '[UNKNOWN_LANGUAGE]' in outs:
                result['reason'] = UNKNOWN_LANGUAGE
            elif '[RUNTIME]' in outs:
                result['reason'] = RESULT_RUNTIME_ERROR
            elif '[COMPILE]' in outs:
                result['reason'] = RESULT_COMPILE_ERROR
            result['last_passed_test_case'] = i
            result['failed_test_case_result'] = outs
            write_result(result)
            sys.exit(0)
        else:
            m = re.search(r"\[MEMORY:(?P<memory>[0-9]+)KB\]\[TIME:(?P<elasped>[0-9]+)ms\]", outs)
            if m:
                max_memory = max(int(m.group('memory')), max_memory)
                max_time = max(int(m.group('elasped')), max_time)
            else:
                result['reason'] = RESULT_RUNTIME_ERROR
                result['last_passed_test_case'] = i
                result['failed_test_case_result'] = outs
                write_result(result)
                sys.exit(0)
            outs = re.sub(r"\[MEMORY:([0-9]+)KB\]\[TIME:([0-9]+)ms\]", "", outs)
            with open(os.path.join(TESTCASE_FOLDER, out_files[i]), 'r') as f:
                raw = f.read().strip()
                if outs == raw:
                    result['reason'] = RESULT_ACCEPTED
                    result['last_passed_test_case'] = len(test_files)
                else:
                    result['reason'] = RESULT_WRONG_ANSWER
                    result['last_passed_test_case'] = i
                    result['failed_test_case_result'] = outs
                    write_result(result)
                    sys.exit(0)
        i += 1
    except TimeoutExpired:
        proc.kill()
        result['last_passed_test_case'] = i
        result['reason'] = RESULT_TIME_EXCEEDED
        write_result(result)
        sys.exit(0)

    result['success'] = True
    result['time'] = max_time
    result['memory'] = max_memory
    write_result(result)
