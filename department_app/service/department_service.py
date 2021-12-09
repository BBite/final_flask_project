"""
Department service used to make database queries, this module defines the following classes:

- `DepartmentService`, department service
"""

from department_app import db
from department_app.models.department import Department
from department_app.schemas.department_schema import DepartmentSchema

from department_app.service.exceptions import UniqueError


class DepartmentService:
    """
    Department service used to make database queries
    """

    schema = DepartmentSchema()

    @staticmethod
    def get_departments() -> list[Department]:
        """
        Fetches all departments from database

        :return: list of all departments
        """
        return db.session.query(Department).all()

    # TODO try add | str and deploy to heroku
    @staticmethod
    def get_department_by_id(department_id: int) -> Department:
        """
        Fetches the department with given id
        if there is no such department return None

        :param department_id: id of the department to be fetched
        :return: department with given id or None
        """
        if not isinstance(department_id, (int, str)) or isinstance(department_id, bool):
            raise TypeError('id should be integer or string')
        return db.session.query(Department).filter_by(id=department_id).first()

    @staticmethod
    def get_department_by_name(name: str) -> Department:
        """
        Fetches the department with given name
        if there is no such department return None

        :param name: name of the department to be fetched
        :return: department with given name or None
        """
        if not isinstance(name, str):
            raise TypeError('name should be string')

        return db.session.query(Department).filter_by(name=name).first()

    @classmethod
    def add_department(cls, department_json) -> Department:
        """
        Deserializes department and adds it to the database

        :param department_json: data to deserialize the department from
        :raise UniqueError: in case of department with given name is already exists
        :return: department that was added
        """
        name = department_json.get('name', None)
        if not isinstance(name, str):
            raise TypeError('name should be string')
        if cls.get_department_by_name(name):
            raise UniqueError('Department with such name is already exists')

        department = cls.schema.load(department_json)
        db.session.add(department)
        db.session.commit()
        return department

    @classmethod
    def update_department(cls, department_id: int, department_json) -> Department:
        """
        Deserializes department and updates department with given id

        :param department_id: id of the department to be updated
        :param department_json: data to deserialize the department from
        :raise ValueError: in case of absence of the department with given id
        :raise UniqueError: in case of department with given name is already exists
        :return: department that was updated
        """
        if not isinstance(department_id, (int, str)) or isinstance(department_id, bool):
            raise TypeError('id should be integer or string')

        department = cls.get_department_by_id(department_id)
        if not department:
            raise ValueError('Invalid department id')

        name = department_json.get('name', None)
        if not isinstance(name, str):
            raise TypeError('name should be string')
        department_in_db = cls.get_department_by_name(department_json.get('name', name))

        if department_in_db and department_in_db != department:
            raise UniqueError('Department with such name is already exists')

        department = cls.schema.load(department_json, instance=department)
        db.session.add(department)
        db.session.commit()
        return department

    @classmethod
    def delete_department(cls, department_id: int) -> None:
        """
        Deletes the department with given id

        :param department_id: id of the department to be deleted
        :raise ValueError: in case of absence of the department with given id
        :return: None
        """
        if not isinstance(department_id, (int, str)) or isinstance(department_id, bool):
            raise TypeError('id should be integer or string')

        department = cls.get_department_by_id(department_id)
        if not department:
            raise ValueError('Invalid department id')

        db.session.delete(department)
        db.session.commit()
