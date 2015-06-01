import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://fcc_admin:fcc_admin@localhost/fcc'

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
    'admin': ('Admin Team', 'admin@heasygame.com'),
    'support': ('Support Team', 'support@heasygame.com')
}
