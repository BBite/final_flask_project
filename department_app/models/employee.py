"""
Employee model used to represent employees, this module defines the following classes:

- `Employee`, employee model
"""

from department_app import db


class Employee(db.Model):
    """
    Model representing employee

    :param str name: employee's name
    :param float salary: employee's salary
    :param date date_of_birth: employee's date of birth
    :param department: department employee works in
    :type department: Department or None
    """

    # pylint: disable=too-few-public-methods

    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date())
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def __init__(self, name, salary, date_of_birth, department=None):
        self.name = name
        self.salary = salary
        self.date_of_birth = date_of_birth
        self.department = department

    def __repr__(self):
        """
        Returns string representation of employee

        :return: string representation of employee
        """
        return f'Employee({self.name}, {self.salary})'
