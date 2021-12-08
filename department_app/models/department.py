"""
Department model used to represent departments, this module defines the following classes:

- `Department`, department model
"""

from department_app import db


class Department(db.Model):
    """
    Model representing department

    :param str name: name of the department
    :param employees: employees working in the department
    :type employees: list[Employee] or None
    """
    # pylint: disable=too-few-public-methods

    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    employees = db.relationship('Employee', lazy=True, backref=db.backref('department', lazy=True))

    def __init__(self, name, employees=None):
        self.name = name
        self.employees = employees or []

    def __repr__(self):
        """
        Returns string representation of department

        :return: string representation of department
        """
        return f'Department({self.name}, {len(self.employees)})'
