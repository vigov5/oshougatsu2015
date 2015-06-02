from flask import g
from flask.ext.admin.contrib.sqla import ModelView

from app.contest.models import Contest


class ContestView(ModelView):

    # Override displayed fields
    column_list = ('name', 'description', 'start_at', 'end_at', 'result_announced_at')
    column_filters = ('name', 'description', 'start_at', 'end_at', 'result_announced_at')

    form_excluded_columns = ('problems', 'scores', 'created_at', 'updated_at')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ContestView, self).__init__(Contest, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()