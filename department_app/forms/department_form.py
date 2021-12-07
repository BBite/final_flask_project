"""
Department form, this module defines the following classes:

- `DepartmentForm`, department form
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from department_app.models.department import Department

from department_app.forms.validators import Unique


class DepartmentForm(FlaskForm):
    """
    Department form
    """
    name = StringField('Name: ',
                       validators=[
                           Length(min=3, max=100,
                                  message="Name should be from 3 up to 100 symbols"),
                           DataRequired(),
                           Unique(Department, Department.name)
                       ])
    submit = SubmitField('')
