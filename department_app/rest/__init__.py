"""
This package contains modules defining department and employee REST APIs and
functions to initialize respective API endpoints:

Modules:
- `department_api.py`: defines department api
- `employee_api.py`: defines employee api

Functions:
- `init_api`: register REST API endpoints
"""

# pylint: disable=cyclic-import

from . import department_api
from . import employee_api


def init_api(api):
    """
    Register REST Api endpoints

    :param api: api to register endpoints
    :return: None
    """
    api.add_resource(
        department_api.DepartmentListApi,
        '/api/departments',
        strict_slashes=False
    )
    api.add_resource(
        department_api.DepartmentApi,
        '/api/department/<int:department_id>',
        strict_slashes=False
    )

    api.add_resource(
        employee_api.EmployeeListApi,
        '/api/employees',
        strict_slashes=False
    )
    api.add_resource(
        employee_api.EmployeeApi,
        '/api/employee/<int:employee_id>', strict_slashes=False
    )
    api.add_resource(
        employee_api.EmployeeSearchApi,
        '/api/employees/search',
        strict_slashes=False
    )
