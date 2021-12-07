"""
Employee service used to make database queries, this module defines the following classes:

- `EmployeeService`, employee service
"""

from department_app import db
from department_app.models.employee import Employee
from department_app.schemas.employee_schema import EmployeeSchema

from department_app.models.department import Department
from department_app.service.department_service import DepartmentService

from department_app.service.exceptions import ExistsError


class EmployeeService:
    """
    Employee service used to make database queries
    """

    schema = EmployeeSchema()

    @staticmethod
    def get_employees() -> list[Employee]:
        """
        Fetches all employees from database

        :return: list of all employees
        """
        return Employee.query.all()

    @staticmethod
    def get_employee_by_id(employee_id: int) -> Employee:
        """
        Fetches the employee with given id
        if there is no such employee return None

        :param employee_id: id of the employee to be fetched
        :return: employee with given id or None
        """
        if not isinstance(employee_id, (int, str)):
            raise TypeError('id should be integer or string')
        return Employee.query.filter_by(id=employee_id).first()

    @staticmethod
    def get_filtered_employees(filter_params: dict) -> list[Employee]:
        """
        Fetches all employees filtered by given params from database

        :param filter_params: params to filter employees by
        :raise ValueError: in case of both the exact date and the period being specified
        :return: list of employees filtered by given params
        """

        # pylint: disable=no-member

        employees = Employee.query
        if filter_params.get('name', None):
            employees = employees.filter(Employee.name.contains(filter_params['name']))
        if filter_params.get('department', None):
            employees = employees.join(Department)
            employees = employees.filter(Department.name.contains(filter_params['department']))
            employees = employees.with_entities(Employee)

        # is not None is used to fix representation as False in case 0
        if filter_params.get('start_salary', None) is not None:
            employees = employees.filter(filter_params['start_salary'] <= Employee.salary)
        if filter_params.get('end_salary', None) is not None:
            employees = employees.filter(filter_params['end_salary'] >= Employee.salary)

        if filter_params.get('start_date', None):
            employees = employees.filter(filter_params['start_date'] <= Employee.date_of_birth)
        if filter_params.get('end_date', None):
            employees = employees.filter(filter_params['end_date'] >= Employee.date_of_birth)

        if filter_params.get('in_date', None):
            if filter_params.get('start_date', None) or filter_params.get('end_date', None):
                raise ValueError('Too much date parameters was given')
            employees = employees.filter(filter_params['in_date'] == Employee.date_of_birth)

        return employees.all()

    @classmethod
    def add_employee(cls, employee_json) -> Employee:
        """
        Deserializes employee and adds it to the database

        :param employee_json: data to deserialize the employee from
        :return: employee that was added
        """
        employee = cls.schema.load(employee_json)
        department = DepartmentService.get_department_by_name(employee_json['department']['name'])
        if not department:
            raise ExistsError('Department with given name does not exist')

        employee.department = department
        db.session.add(employee)
        db.session.commit()
        return employee

    @classmethod
    def update_employee(cls, employee_id: int, employee_json) -> Employee:
        """
        Deserializes employee and updates employee with given id

        :param employee_id: id of the employee to be updated
        :param employee_json: data to deserialize the employee from
        :raise ValueError: in case of absence of the employee with given id
        :raise UniqueError: in case of department with given name does not exist
        :return: employee that was updated
        """
        if not isinstance(employee_id, (int, str)):
            raise TypeError('id should be integer or string')

        employee = cls.get_employee_by_id(employee_id)
        if not employee:
            raise ValueError('Invalid employee id')

        employee = cls.schema.load(employee_json, instance=employee)
        department = DepartmentService.get_department_by_name(employee_json['department']['name'])
        if not department:
            raise ExistsError('Department with given name does not exist')

        employee.department = department

        db.session.add(employee)
        db.session.commit()
        return employee

    @classmethod
    def delete_employee(cls, employee_id: int) -> None:
        """
        Deletes the employee with given id

        :param employee_id: id of the employee to be deleted
        :raise ValueError: in case of absence of the employee with given id
        :return: None
        """
        if not isinstance(employee_id, (int, str)):
            raise TypeError('id should be integer or string')

        employee = cls.get_employee_by_id(employee_id)
        if not employee:
            raise ValueError('Invalid employee id')

        db.session.delete(employee)
        db.session.commit()
