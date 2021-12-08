"""
This module defines is used to populate database with departments and employees,
it defines the following:

Functions:
- `populate_db`: populate database with departments and employees
"""

from datetime import date

from department_app import app, db

from department_app.models.department import Department
from department_app.models.employee import Employee


def populate_db():
    """
    Populate database with departments and employees

    :return: None
    """
    department_1 = Department('Research')
    department_2 = Department('Purchase')
    department_3 = Department('Human Resource')
    department_4 = Department('Finance')
    department_5 = Department('Marketing')

    employee_1 = Employee('Marty Maxwell', 700, date(2002, 5, 4), department_3)
    employee_2 = Employee('Erin Dolton', 4000, date(2002, 6, 3), department_1)
    employee_3 = Employee('Alex Marshman', 250, date(1989, 11, 30), department_2)
    employee_4 = Employee('Tilda Robson', 375, date(2000, 10, 1), department_3)
    employee_5 = Employee('Lois Gordon', 1000, date(2002, 10, 3), department_4)
    employee_6 = Employee('Geoffrey Vaughn', 2800, date(1993, 2, 23), department_5)
    employee_7 = Employee('Harry Tyler', 1200, date(1989, 11, 30), department_4)
    employee_8 = Employee('Dean Farmer', 4500, date(2002, 10, 4), department_1)
    employee_9 = Employee('Webster Robson', 500, date(1996, 5, 12), department_2)
    employee_10 = Employee('Leon Stevens', 900, date(1980, 2, 23), department_2)

    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)
    db.session.add(department_4)
    db.session.add(department_5)

    db.session.add(employee_1)
    db.session.add(employee_2)
    db.session.add(employee_3)
    db.session.add(employee_4)
    db.session.add(employee_5)
    db.session.add(employee_6)
    db.session.add(employee_7)
    db.session.add(employee_8)
    db.session.add(employee_9)
    db.session.add(employee_10)

    db.session.commit()
    db.session.close()
    app.logger.info('Database was successfully populated')


if __name__ == '__main__':
    populate_db()
