"""
Departments REST API, this module defines the following classes:

- `EmployeeApiBase`, employee API base class
- `EmployeeSearchApi`, employee search API class
- `EmployeeListApi`, employee list API class
- `EmployeeApi`, employee API class
"""

from datetime import datetime

from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from department_app import app
from department_app.schemas.employee_schema import EmployeeSchema
from department_app.service.employee_service import EmployeeService

from department_app.service.exceptions import ExistsError


def get_date_or_none(date_str, date_format='%d.%m.%Y'):
    """
    Returns date represented by date string and date format or
    None if date string has wrong type/doesn't match the format specified

    :param date_str: date string to convert into date object
    :param date_format: format of the date string
    :return: date object constructed from date string using date format or
    None in case of being unable to construct date object
    """
    try:
        return datetime.strptime(date_str, date_format).date()
    except (ValueError, TypeError):
        return None


class EmployeeApiBase(Resource):
    """
    Employee API base class
    """
    # Marshmallow schema used for employee serialization/deserialization
    schema = EmployeeSchema()

    # employee database service
    service = EmployeeService()


class EmployeeListApi(EmployeeApiBase):
    """
    Employee search list API class
    """
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('department', type=dict)
    parser.add_argument('salary', type=float)
    parser.add_argument('date_of_birth',
                        type=lambda date_str: get_date_or_none(date_str).strftime('%d.%m.%Y'))

    def get(self):
        """
        GET request handler of employee list API

        Fetches all employees via service
        Returns them in a JSON format with a status code 200(OK)

        :return: list of all employees JSON and a status code 200
        """
        employees = self.service.get_employees()
        employees = self.schema.dump(employees, many=True)
        app.logger.debug(f'Returned: {employees}')
        return employees, 200

    def post(self):
        """
        POST request handler of employee list API

        Deserializes request data
        Uses service to add the employee to the database
        Returns added employee in a JSON format with a status code 201(Created) or
        error messages with a status code 400(Bad Request)
        in case of validation error during deserialization

        :return: added employee JSON and status code 201 or
        error message and status code 400 in case of validation error
        """
        try:
            data = self.parser.parse_args()
            app.logger.debug(f'Received: {data}')
            employee = self.service.add_employee(data)
        except ValidationError as error:
            app.logger.error(error.messages)
            return error.messages, 400
        except (ExistsError, TypeError) as error:
            app.logger.error(str(error))
            return str(error), 400
        employee = self.schema.dump(employee)
        app.logger.debug(f'Returned: {employee}')
        return employee, 201


class EmployeeApi(EmployeeApiBase):
    """
    Employee API class
    """
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('department', type=dict)
    parser.add_argument('salary', type=float)
    parser.add_argument('date_of_birth',
                        type=lambda date_str: get_date_or_none(date_str).strftime('%d.%m.%Y'))

    def get(self, employee_id: int):
        """
        GET request handler of employee API

        Fetches the employee with given id via service
        Returns it in a JSON format with a status code 200(OK) or
        error message with a status code 404(Not Found)
        in case of employee with given id not being found

        :return: employee with given id in JSON and a status code 200 or
        error message and a status code 404 in case of employee with given id not being found
        """
        try:
            app.logger.debug(f'Employee id: {employee_id}')
            employee = self.service.get_employee_by_id(employee_id)
        except ValueError:
            app.logger.error('Employee not found')
            return 'Employee not found', 404
        employee = self.schema.dump(employee)
        app.logger.debug(f'Returned: {employee}')
        return employee, 200

    def put(self, employee_id: int):
        """
        PUT request handler of employee API

        Uses service to deserialize request data and find the employee with given id
        Updates it with deserialized instance
        Returns updated employee in a JSON format with a status code 201(Created) or
        error message with a status code 400(Bad Request)
        in case of validation error during deserialization or
        error message with a status code 404(Not Found)
        in case of employee with given id not being found

        :return: updated employee JSON and status code 200 or
        error message and status code 400 in case of validation error or
        error message and a status code 404 in case of employee with given id not being found
        """
        try:
            app.logger.debug(f'Employee id: {employee_id}')
            data = self.parser.parse_args()
            app.logger.debug(f'Received: {data}')
            employee = self.service.update_employee(employee_id, data)
        except ValidationError as error:
            app.logger.error(error.messages)
            return error.messages, 400
        except ValueError:
            app.logger.error('Employee not found')
            return 'Employee not found', 404
        except (ExistsError, TypeError) as error:
            app.logger.error(str(error))
            return str(error), 400
        employee = self.schema.dump(employee)
        app.logger.debug(f'Returned: {employee}')
        return employee, 200

    def delete(self, employee_id: int):
        """
        DELETE request handler of employee API

        Uses service to delete the employee with given id
        Returns no content message with a status code 204(No Content) or
        error message with a status code 404(Not Found)
        in case of employee with given id not being found

        :return: no content message and status code 204 or
        error message and a status code 404 in case of employee with given id not being found
        """
        try:
            app.logger.debug(f'Employee id: {employee_id}')
            self.service.delete_employee(employee_id)
        except ValueError:
            app.logger.error('Employee not found')
            return 'Employee not found', 404
        return '', 204


class EmployeeSearchApi(EmployeeApiBase):
    """
    Employee search API class
    """
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('department', type=str)
    parser.add_argument('start_salary', type=float)
    parser.add_argument('end_salary', type=float)

    # pylint: disable=unnecessary-lambda
    parser.add_argument('start_date', type=lambda date_str: get_date_or_none(date_str))
    parser.add_argument('end_date', type=lambda date_str: get_date_or_none(date_str))
    parser.add_argument('in_date', type=lambda date_str: get_date_or_none(date_str))

    def get(self):
        """
        GET request handler of employee search API

        Fetches the employees filtered by given params via service
        Unspecified parameters will not filter the result
        Returns them in a JSON format with a status code 200(OK) or
        error message with a status code 400(Bad Request)
        in case of both the exact date and the period being specified

        :return: list of the employees filtered by given params in JSON and a status code 200 or
        error message and a status code 400
        in case of both the exact date and the period being specified
        """
        try:
            data = self.parser.parse_args()
            app.logger.debug(f'Received: {data}')
            employees = self.service.get_filtered_employees(data)
        except ValueError as error:
            app.logger.error(str(error))
            return str(error), 400
        employees = self.schema.dump(employees, many=True)
        app.logger.debug(f'Returned: {employees}')
        return employees, 200
