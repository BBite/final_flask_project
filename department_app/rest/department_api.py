"""
Departments REST API, this module defines the following classes:

- `DepartmentApiBase`, department API base class
- `DepartmentListApi`, department list API class
- `DepartmentApi`, department API class
"""

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from department_app import app
from department_app.schemas.department_schema import DepartmentSchema
from department_app.service.department_service import DepartmentService

from department_app.service.exceptions import UniqueError


class DepartmentApiBase(Resource):
    """
    Department API base class
    """
    # Marshmallow schema used for department serialization/deserialization
    schema = DepartmentSchema()

    # department database service
    service = DepartmentService()


class DepartmentListApi(DepartmentApiBase):
    """
    Department list API class
    """

    def get(self):
        """
        GET request handler of department list API

        Fetches all departments via service
        Returns them in a JSON format with a status code 200(OK)

        :return: list of all departments JSON and a status code 200
        """
        departments = self.service.get_departments()
        departments = self.schema.dump(departments, many=True)
        app.logger.debug(f'Returned: {departments}')
        return departments, 200

    def post(self):
        """
        POST request handler of department list API

        Deserializes request data
        Uses service to add the department to the database
        Returns added department in a JSON format with a status code 201(Created) or
        error messages with a status code 400(Bad Request)
        in case of validation error during deserialization

        :return: added department JSON and status code 201 or
        error message and status code 400 in case of validation error
        """
        try:
            data = request.json
            app.logger.debug(f'Received: {data}')
            department = self.service.add_department(data)
        except ValidationError as error:
            app.logger.error(error.messages)
            return error.messages, 400
        except (UniqueError, TypeError) as error:
            app.logger.error(str(error))
            return str(error), 400

        department = self.schema.dump(department)
        app.logger.debug(f'Returned: {department}')
        return department, 201


class DepartmentApi(DepartmentApiBase):
    """
    Department API class
    """

    def get(self, department_id: int):
        """
        GET request handler of department API

        Fetches the department with given id via service
        Returns it in a JSON format with a status code 200(OK) or
        returns an error message with a status code 404(Not Found)
        in case of department with given id not being found

        :param int department_id: id of the department
        :return: department with given id in JSON and a status code 200 or
        error message and a status code 404 in case of department with given id not being found
        """
        try:
            app.logger.debug(f'Department id: {department_id}')
            department = self.service.get_department_by_id(department_id)
        except ValueError:
            app.logger.error('Department not found')
            return 'Department not found', 404
        department = self.schema.dump(department)
        app.logger.debug(f'Returned: {department}')
        return department, 200

    def put(self, department_id: int):
        """
        PUT request handler of department API

        Uses service to deserialize request data and find the department with given id
        Updates it with deserialized instance
        Returns updated department in a JSON format with a status code 201(Created) or
        error messages with a status code 400(Bad Request)
        in case of validation error during deserialization or
        error message with a status code 404(Not Found)
        in case of department with given id not being found

        :param int department_id: id of the department to be updated
        :return: updated department JSON and status code 200 or
        error message and status code 400 in case of validation error or
        error message and a status code 404 in case of department with given id not being found
        """
        try:
            app.logger.debug(f'Department id: {department_id}')
            data = request.json
            app.logger.debug(f'Received: {data}')
            department = self.service.update_department(department_id, data)
        except ValidationError as error:
            app.logger.error(error.messages)
            return error.messages, 400
        except (UniqueError, TypeError) as error:
            app.logger.error(str(error))
            return str(error), 400
        except ValueError:
            app.logger.error('Department not found')
            return 'Department not found', 404
        return self.schema.dump(department), 200

    def delete(self, department_id: int):
        """
        DELETE request handler of department API

        Uses service to delete the department with given id
        Returns no content message with a status code 204(No Content) or
        error message with a status code 404(Not Found)
        in case of department with given id not being found

        :param int department_id: id of the department to be deleted
        :return: no content message and status code 204 or
        error message and a status code 404 in case of department with given id not being found
        """
        try:
            app.logger.debug(f'Department id: {department_id}')
            self.service.delete_department(department_id)
        except ValueError:
            app.logger.error('Department not found')
            return 'Department not found', 404
        return '', 204
