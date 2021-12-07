"""
Employee schema used to serialize/deserialize departments,
this module defines the following classes:

- `EmployeeSchema`, employee serialization/deserialization schema
"""

from marshmallow import fields, EXCLUDE

from department_app import ma

from department_app.models.employee import Employee
from department_app.schemas.department_schema import DepartmentSchema


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    """
    Employee serialization/deserialization schema
    """

    # pylint: disable=too-few-public-methods, too-many-ancestors

    class Meta:
        """
        Employee schema metadata
        """
        model = Employee
        exclude = ('department_id',)
        load_instance = True
        include_fk = True
        dateformat = '%d.%m.%Y'
        dump_only = ('id', 'department')  # fields to provide only on serialization
        unknown = EXCLUDE

    department = fields.Nested(DepartmentSchema(only=('name',)))
