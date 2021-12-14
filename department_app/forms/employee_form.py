"""
Department form, this module defines the following classes:

- `EmployeeForm`, employee form
- `FilterForm`, filter form
"""

from datetime import date
from dateutil.relativedelta import relativedelta

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, RadioField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Optional

from department_app.models.department import Department

from department_app.forms.validators import Exists


class EmployeeForm(FlaskForm):
    """
    Employee form
    """
    name = StringField('Name: ',
                       validators=[
                           Length(min=3, max=50, message="Name should be from 3 up to 50 symbols"),
                           DataRequired()
                       ])
    department = StringField('Department: ',
                             validators=[
                                 Length(min=3, max=50,
                                        message="Department should be from 3 up to 50 symbols"),
                                 DataRequired(),
                                 Exists(Department, Department.name)
                             ])
    salary = DecimalField('Salary: ',
                          validators=[
                              NumberRange(min=0, max=100_000, message='Salary should be positive'),
                              DataRequired()
                          ])
    date_of_birth = DateField('Date of Birth:', validators=[DataRequired()])
    submit = SubmitField('')

    max_date = date.today() - relativedelta(years=18)

    def with_department(self):
        """
        Deletes department field from form
        """
        del self.department


class FilterForm(FlaskForm):
    """
    Filter form
    """
    name = StringField('Name', validators=[Optional()])
    department = StringField('Department', validators=[Optional()])

    start_salary = DecimalField('From:',
                                validators=[
                                    NumberRange(min=0, message='Salary should be positive'),
                                    Optional()
                                ])
    end_salary = DecimalField('To:',
                              validators=[
                                  NumberRange(min=0, message='Salary should be positive'),
                                  Optional()
                              ])

    date_input_type = RadioField(choices=['in', 'between'], default='in')

    start_date = DateField(validators=[Optional()])
    end_date = DateField(validators=[Optional()])
    submit = SubmitField('Search')

    # maximum valid date of birth of employee
    max_date = date.today() - relativedelta(years=18)

    def validate_end_salary(self, field):
        """
        Validation for end_salary field
        """
        if field.data and self.start_salary.data and field.data < self.start_salary.data:
            raise ValidationError('end salary must be less than start salary')

    def validate_end_date(self, field):
        """
        Validation for end_date field
        """
        if (field.data and self.start_date.data and field.data < self.start_date.data
                and self.date_input_type.data == 'between'):
            raise ValidationError('end date must be later than start date')
