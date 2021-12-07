"""
This package contains modules defining department and employee views:

Modules:
- `department_view.py`: defines department views
- `employee_view.py`: defines employee views
- `error_view.py`: defines error views

Functions:
- `init_blueprints`: register blueprints endpoints
"""

# pylint: disable=cyclic-import

from . import department_view
from . import employee_view
from . import error_view


def init_blueprints(app):
    """
    Register blueprints endpoints

    :param app: app to register endpoints
    :return: None
    """
    app.register_blueprint(department_view.departments_blueprint)
    app.register_blueprint(employee_view.employees_blueprint)
