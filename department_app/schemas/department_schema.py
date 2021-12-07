"""
Department schema used to serialize/deserialize departments,
this module defines the following classes:

- `DepartmentSchema`, department serialization/deserialization schema
"""

from marshmallow import fields, EXCLUDE

from department_app import ma

from department_app.models.department import Department


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    """
    Department serialization/deserialization schema
    """

    # pylint: disable=too-few-public-methods, too-many-ancestors

    class Meta:
        """
        Department schema metadata
        """
        model = Department
        load_instance = True
        include_fk = True
        dump_only = ('id', 'employees')  # fields to provide only on serialization
        unknown = EXCLUDE

    # average salary of the department employees
    avg_salary = fields.Method('calculate_avg_salary')

    employees = fields.Nested(
        'EmployeeSchema', many=True, exclude=('department',)
    )

    @staticmethod
    def calculate_avg_salary(department: Department) -> float:
        """
        Returns average salary of the department employees

        :param Department department: department to calculate average salary for
        :return: average salary of the department employees
        """
        try:
            return round(sum(map(lambda employee: employee.salary, department.employees))
                         / len(department.employees), 2)
        except ZeroDivisionError:
            return 0
