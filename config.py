import os

from app.submission import constants as SUBMISSION

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://fcc_admin:fcc_admin@localhost/bk'

CSRF_ENABLED = True
SECRET_KEY = 'place_your_secret_here'
CSRF_SESSION_KEY = 'place_your_csrf_key_here'

# mail config
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
# MAIL_DEBUG = app.debug
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = None
MAIL_MAX_EMAILS = None
# MAIL_SUPPRESS_SEND = app.testing
MAIL_ASCII_ATTACHMENTS = False

MAIL_TEMPLATE_FOLDER = 'mails'

MAIL_SENDERS = {
    'admin': ('Admin Team', 'admin@ctf.framgia.vn'),
    'support': ('Support Team', 'support@ctf.framgia.vn')
}

ADMINS = [
	'nguyen.anh.tien@framgia.com',
	'tran.ba.trong@framgia.com'
]

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

TESTCASE_FOLDER = os.path.join(basedir, 'shared', 'testcases')
SUBMISSION_FOLDER = os.path.join(basedir, 'shared', 'submissions')
RUN_FOLDER = os.path.join(basedir, 'run')
PAYLOAD_FOLDER = os.path.join(basedir, 'payload')

UPLOADED_CODE_DEST = os.path.join(basedir, 'tmp')
UPLOADED_FILES_ALLOW = SUBMISSION.LANG_EXTENSIONS.values()


CONTEST_DURATION = 15