from flask import g
from flask_admin.contrib.sqla import ModelView

from app.problem.models import Problem

class ProblemView(ModelView):

    column_default_sort = ('id', True)

    # Override displayed fields
    column_list = ('id', 'contest.name', 'name_en', 'name_vi', 'rank')

    form_excluded_columns = ('submissions', 'created_at', 'updated_at')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ProblemView, self).__init__(Problem, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
