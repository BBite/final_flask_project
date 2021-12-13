# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from datetime import date

from flask_testing import TestCase

from department_app import app, db

from department_app.models.department import Department
from department_app.models.employee import Employee


class BaseTestCase(TestCase):
    """A base test case"""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        department_1 = Department('Research')

        employee_1 = Employee('Marty Maxwell', 700, date(2002, 5, 4), department_1)

        db.session.add(department_1)

        db.session.add(employee_1)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class SearchBaseTestCase(BaseTestCase):
    """A search employee base test case"""

    def setUp(self):
        db.create_all()
        department_1 = Department('Research')
        department_2 = Department('Purchase')

        employee_1 = Employee('Marty Maxwell', 700, date(2002, 5, 4), department_1)
        employee_2 = Employee('Erin Dolton', 4000, date(2002, 6, 3), department_2)
        employee_3 = Employee('Alex Marshman', 250, date(1989, 11, 30), department_2)

        db.session.add(department_1)
        db.session.add(department_2)

        db.session.add(employee_1)
        db.session.add(employee_2)
        db.session.add(employee_3)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
