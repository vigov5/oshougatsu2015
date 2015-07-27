from flask import g, Blueprint
from flask_admin.contrib.sqla import ModelView

from app.hint.models import Hint


class HintView(ModelView):

    column_default_sort = ('id', True)

    # Override displayed fields
    column_list = ('id', 'problem.id', 'problem.name_en', 'description', 'is_open')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(HintView, self).__init__(Hint, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
