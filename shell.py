#!venv/bin/python

import os
import readline
from pprint import pprint
import rlcompleter, readline

from flask import *
from app import *
from app.contest.models import *
from app.problem.models import *
from app.submission.models import *
from app.user.models import *

os.environ['PYTHONINSPECT'] = 'True'
readline.parse_and_bind('tab:complete')
