# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=no-self-use, too-many-statements


import json
from unittest.mock import patch

from datetime import date
from marshmallow import ValidationError

from department_app.rest.employee_api import get_date_or_none

from department_app.service.exceptions import ExistsError

from department_app.tests.base import BaseTestCase
from department_app.tests.data import employee_1, employee_2
from department_app.tests.data import employee_to_json, employees_to_json


class TestEmployeeApi(BaseTestCase):
    def test_get_employees(self):
        expected_employees = [employee_1]
        expected_json = employees_to_json(expected_employees)

        with patch(
                'department_app.rest.employee_api.EmployeeService.get_employees',
                autospec=True, return_value=expected_employees
        ) as get_employees_mock, patch(
            'department_app.rest.employee_api.EmployeeListApi.schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get('api/employees')

            self.assert200(response)
            self.assertCountEqual(expected_json, response.json)

            get_employees_mock.assert_called_once()
            schema_mock.assert_called_once_with(expected_employees, many=True)
            logger_mock.debug.assert_called_once()

    def test_get_employee_success(self):
        expected_employee = employee_1
        expected_json = employee_to_json(expected_employee)
        employee_id = 1

        with patch(
                'department_app.rest.employee_api.EmployeeService.get_employee_by_id',
                autospec=True, return_value=expected_employee
        ) as get_employee_by_id_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'api/employee/{employee_id}')

            self.assert200(response)
            self.assertDictEqual(expected_json, response.json)

            get_employee_by_id_mock.assert_called_once_with(employee_id)
            schema_mock.assert_called_once_with(expected_employee)
            logger_mock.debug.assert_called()

    def test_get_employee_failure(self):
        expected_message = 'Employee not found'
        employee_id = 0

        with patch(
                'department_app.rest.employee_api.EmployeeService.get_employee_by_id',
                autospec=True, side_effect=ValueError
        ) as get_employee_by_id_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump',
            autospec=True
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'api/employee/{employee_id}')

            self.assert404(response)
            self.assertEqual(expected_message, response.json)

            get_employee_by_id_mock.assert_called_once_with(employee_id)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_called_once()

    def test_post_employee_success(self):
        expected_employee = employee_2
        data = expected_json = employee_to_json(expected_employee)

        with patch(
                'department_app.rest.employee_api.EmployeeService.add_employee',
                autospec=True, return_value=expected_employee
        ) as add_employee_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/api/employees',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assertStatus(response, 201)
            self.assertDictEqual(expected_json, response.json)

            add_employee_mock.assert_called_once_with(data)
            schema_mock.assert_called_once_with(expected_employee)
            logger_mock.debug.assert_called()

    def test_post_employee_failure(self):
        expected_message = 'Test ExistsError message'
        data = employee_to_json(employee_1)
        data['department'] = {'name': 'bad name'}

        with patch(
                'department_app.rest.employee_api.EmployeeService.add_employee',
                autospec=True, side_effect=ExistsError(expected_message)
        ) as add_employee_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump', autospec=True,
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/api/employees',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert400(response)
            self.assertEqual(expected_message, response.json)

            add_employee_mock.assert_called_once_with(data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_called_once()

        expected_message = 'Test TypeError message'
        data = employee_to_json(employee_1)
        data['name'] = 'bad name'

        with patch(
                'department_app.rest.employee_api.EmployeeService.add_employee',
                autospec=True, side_effect=TypeError(expected_message)
        ) as add_employee_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump', autospec=True,
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/api/employees',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert400(response)
            self.assertEqual(expected_message, response.json)

            add_employee_mock.assert_called_once_with(data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_called_once()

        expected_message = 'Test ValidationError message'
        data = employee_to_json(employee_1)

        with patch(
                'department_app.rest.employee_api.EmployeeService.add_employee',
                autospec=True, side_effect=ValidationError(expected_message)
        ) as add_employee_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump', autospec=True,
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/api/employees',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert400(response)
            self.assertEqual(ValidationError(expected_message).messages, response.json)

            add_employee_mock.assert_called_once_with(data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_called_once()

    def test_put_employee_success(self):
        expected_employee = employee_1
        data = expected_json = employee_to_json(expected_employee)
        employee_id = 1

        with patch(
                'department_app.rest.employee_api.EmployeeService.update_employee',
                autospec=True, return_value=expected_employee
        ) as update_employee_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.put(f'/api/employee/{employee_id}',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert200(response)
            self.assertDictEqual(expected_json, response.json)

            update_employee_mock.assert_called_once_with(employee_id, data)
            schema_mock.assert_called_once_with(expected_employee)
            logger_mock.debug.assert_called()

    def test_put_employee_failure(self):
        employee_id = 1
        expected_message = 'Test UniqueError message'
        data = employee_to_json(employee_1)
        data['department'] = {'name': 'bad name'}

        with patch(
                'department_app.rest.employee_api.EmployeeService.update_employee',
                autospec=True, side_effect=ExistsError(expected_message)
        ) as update_employee_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.put(f'/api/employee/{employee_id}',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert400(response)
            self.assertEqual(expected_message, response.json)

            update_employee_mock.assert_called_once_with(employee_id, data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

        expected_message = 'Test TypeError message'
        data = employee_to_json(employee_1)
        data['name'] = 'bad name'

        with patch(
                'department_app.rest.employee_api.EmployeeService.update_employee',
                autospec=True, side_effect=TypeError(expected_message)
        ) as update_employee_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.put(f'/api/employee/{employee_id}',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert400(response)
            self.assertEqual(expected_message, response.json)

            update_employee_mock.assert_called_once_with(employee_id, data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

        expected_message = 'Test ValidationError message'
        data = employee_to_json(employee_1)
        data['name'] = 'bad name'

        with patch(
                'department_app.rest.employee_api.EmployeeService.update_employee',
                autospec=True, side_effect=ValidationError(expected_message)
        ) as update_employee_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.put(f'/api/employee/{employee_id}',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert400(response)
            self.assertEqual(ValidationError(expected_message).messages, response.json)

            update_employee_mock.assert_called_once_with(employee_id, data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

        expected_message = 'Employee not found'
        data = employee_to_json(employee_1)
        data['name'] = 'bad name'

        with patch(
                'department_app.rest.employee_api.EmployeeService.update_employee',
                autospec=True, side_effect=ValueError(expected_message)
        ) as update_employee_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.put(f'/api/employee/{employee_id}',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert404(response)
            self.assertEqual(expected_message, response.json)

            update_employee_mock.assert_called_once_with(employee_id, data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

    def test_delete_employee_success(self):
        expected_message = ''
        employee_id = 1

        with patch(
                'department_app.rest.employee_api.EmployeeService.delete_employee',
                autospec=True
        ) as delete_employee_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.delete(f'/api/employee/{employee_id}')

            self.assertStatus(response, 204)
            self.assertEqual(expected_message, response.get_data(as_text=True))

            delete_employee_mock.assert_called_once_with(employee_id)
            logger_mock.debug.assert_called_once()

    def test_delete_employee_failure(self):
        expected_message = 'Employee not found'
        employee_id = 1

        with patch(
                'department_app.rest.employee_api.EmployeeService.delete_employee',
                autospec=True, side_effect=ValueError
        ) as delete_employee_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.delete(f'/api/employee/{employee_id}')

            self.assert404(response)
            self.assertEqual(expected_message, response.json)

            delete_employee_mock.assert_called_once_with(employee_id)
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_called_once()

    def test_search_success(self):
        expected_employees = [employee_1, employee_2]
        expected_json = employees_to_json(expected_employees)

        data = {
            'name': 'test name',
            'department': 'test department',
            'start_salary': 0,
            'end_salary': 5000,
            'start_date': '12.04.2002',
            'end_date': '12.05.2002',
            'in_date': None
        }

        parsed_data = data.copy()
        parsed_data['start_date'] = date(2002, 4, 12)
        parsed_data['end_date'] = date(2002, 5, 12)

        with patch(
                'department_app.rest.employee_api.EmployeeService.get_filtered_employees',
                autospec=True, return_value=expected_employees
        ) as get_filtered_employees_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get('/api/employees/search',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert200(response)
            self.assertCountEqual(expected_json, response.json)

            get_filtered_employees_mock.assert_called_once_with(parsed_data)
            schema_mock.assert_called_once_with(expected_employees, many=True)
            logger_mock.debug.assert_called()

    def test_search_failure(self):
        expected_message = 'Test ValueError message'

        data = {
            'name': 'test name',
            'department': 'test department',
            'start_salary': 1000,
            'end_salary': 500,
            'start_date': '12.04.2002',
            'end_date': '12.05.2002',
            'in_date': None
        }

        parsed_data = data.copy()
        parsed_data['start_date'] = date(2002, 4, 12)
        parsed_data['end_date'] = date(2002, 5, 12)

        with patch(
                'department_app.rest.employee_api.EmployeeService.get_filtered_employees',
                autospec=True, side_effect=ValueError(expected_message)
        ) as get_filtered_employees_mock, patch(
            'department_app.rest.employee_api.EmployeeApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.employee_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get('/api/employees/search',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert400(response)
            self.assertEqual(expected_message, response.json)

            get_filtered_employees_mock.assert_called_once_with(parsed_data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_called_once()

    def test_get_date_or_none_success(self):
        date_str = '11.10.2012'
        exepected_date = date(2012, 10, 11)
        result = get_date_or_none(date_str)
        self.assertEqual(exepected_date, result)

    def test_get_date_or_none_failure(self):
        date_str = 1
        result = get_date_or_none(date_str)
        self.assertIsNone(result)
