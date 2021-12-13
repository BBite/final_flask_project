# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import json
from unittest.mock import patch

from marshmallow import ValidationError

from department_app.tests.base import BaseTestCase

from department_app.service.exceptions import UniqueError

from department_app.tests.data import department_1, department_2
from department_app.tests.data import department_to_json, departments_to_json


class TestDepartmentApi(BaseTestCase):
    def test_get_departments(self):
        expected_departments = [department_1]
        expected_json = departments_to_json(expected_departments)

        with patch(
                'department_app.rest.department_api.DepartmentService.get_departments',
                autospec=True, return_value=expected_departments
        ) as get_departments_mock, patch(
            'department_app.rest.department_api.DepartmentListApi.schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get('api/departments')

            self.assert200(response)
            self.assertCountEqual(expected_json, response.json)

            get_departments_mock.assert_called_once()
            schema_mock.assert_called_once_with(expected_departments, many=True)
            logger_mock.debug.assert_called_once()

    def test_get_department_success(self):
        expected_department = department_1
        expected_json = department_to_json(expected_department)
        department_id = 1

        with patch(
                'department_app.rest.department_api.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_by_id_mock, patch(
            'department_app.rest.department_api.DepartmentApi.schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'api/department/{department_id}')

            self.assert200(response)
            self.assertDictEqual(expected_json, response.json)

            get_department_by_id_mock.assert_called_once_with(department_id)
            schema_mock.assert_called_once_with(expected_department)
            logger_mock.debug.assert_called()

    def test_get_department_failure(self):
        expected_message = 'Department not found'
        department_id = 0

        with patch(
                'department_app.rest.department_api.DepartmentService.get_department_by_id',
                autospec=True, side_effect=ValueError
        ) as get_department_by_id_mock, patch(
            'department_app.rest.department_api.DepartmentApi.schema.dump',
            autospec=True
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'api/department/{department_id}')

            self.assert404(response)
            self.assertEqual(expected_message, response.json)

            get_department_by_id_mock.assert_called_once_with(department_id)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_called_once()

    def test_post_department_success(self):
        expected_department = department_2
        data = expected_json = department_to_json(expected_department)

        with patch(
                'department_app.rest.department_api.DepartmentService.add_department',
                autospec=True, return_value=expected_department
        ) as add_department_mock, patch(
            'department_app.rest.department_api.DepartmentApi.schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/api/departments',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assertStatus(response, 201)
            self.assertDictEqual(expected_json, response.json)

            add_department_mock.assert_called_once_with(data)
            schema_mock.assert_called_once_with(expected_department)
            logger_mock.debug.assert_called()

    def test_post_department_failure(self):
        expected_message = 'Test UniqueError message'
        data = {'name': 'used name'}

        with patch(
                'department_app.rest.department_api.DepartmentService.add_department',
                autospec=True, side_effect=UniqueError(expected_message)
        ) as add_department_mock, patch(
            'department_app.rest.department_api.DepartmentApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/api/departments',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert400(response)
            self.assertEqual(expected_message, response.json)

            add_department_mock.assert_called_once_with(data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_called_once()

        expected_message = 'Test TypeError message'
        data = {'name': 1}

        with patch(
                'department_app.rest.department_api.DepartmentService.add_department',
                autospec=True, side_effect=TypeError(expected_message)
        ) as add_department_mock, patch(
            'department_app.rest.department_api.DepartmentApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/api/departments',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert400(response)
            self.assertEqual(expected_message, response.json)

            add_department_mock.assert_called_once_with(data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_called_once()

        expected_message = 'Test ValidationError message'
        data = {'name': 1}

        with patch(
                'department_app.rest.department_api.DepartmentService.add_department',
                autospec=True, side_effect=ValidationError(expected_message)
        ) as add_department_mock, patch(
            'department_app.rest.department_api.DepartmentApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/api/departments',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert400(response)
            self.assertEqual(ValidationError(expected_message).messages, response.json)

            add_department_mock.assert_called_once_with(data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_called_once()

    def test_put_department_success(self):
        expected_department = department_1
        data = expected_json = department_to_json(expected_department)
        department_id = 1

        with patch(
                'department_app.rest.department_api.DepartmentService.update_department',
                autospec=True, return_value=expected_department
        ) as update_department_mock, patch(
            'department_app.rest.department_api.DepartmentApi.schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.put(f'/api/department/{department_id}',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert200(response)
            self.assertDictEqual(expected_json, response.json)

            update_department_mock.assert_called_once_with(department_id, data)
            schema_mock.assert_called_once_with(expected_department)
            logger_mock.debug.assert_called()

    def test_put_department_failure(self):
        department_id = 2
        expected_message = 'Test UniqueError message'
        data = {'name': 'used name'}

        with patch(
                'department_app.rest.department_api.DepartmentService.update_department',
                autospec=True, side_effect=UniqueError(expected_message)
        ) as update_department_mock, patch(
            'department_app.rest.department_api.DepartmentApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.put(f'/api/department/{department_id}',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert400(response)
            self.assertEqual(expected_message, response.json)

            update_department_mock.assert_called_once_with(department_id, data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

        expected_message = 'Test TypeError message'
        data = {'name': 'used name'}

        with patch(
                'department_app.rest.department_api.DepartmentService.update_department',
                autospec=True, side_effect=TypeError(expected_message)
        ) as update_department_mock, patch(
            'department_app.rest.department_api.DepartmentApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.put(f'/api/department/{department_id}',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert400(response)
            self.assertEqual(expected_message, response.json)

            update_department_mock.assert_called_once_with(department_id, data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

        expected_message = 'Test ValidationError message'
        data = {'name': 'used name'}

        with patch(
                'department_app.rest.department_api.DepartmentService.update_department',
                autospec=True, side_effect=ValidationError(expected_message)
        ) as update_department_mock, patch(
            'department_app.rest.department_api.DepartmentApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.put(f'/api/department/{department_id}',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert400(response)
            self.assertEqual(ValidationError(expected_message).messages, response.json)

            update_department_mock.assert_called_once_with(department_id, data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

        expected_message = 'Department not found'
        data = {'name': 'used name'}

        with patch(
                'department_app.rest.department_api.DepartmentService.update_department',
                autospec=True, side_effect=ValueError
        ) as update_department_mock, patch(
            'department_app.rest.department_api.DepartmentApi.schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.put(f'/api/department/{department_id}',
                                       data=json.dumps(data),
                                       content_type='application/json')

            self.assert404(response)
            self.assertEqual(expected_message, response.json)

            update_department_mock.assert_called_once_with(department_id, data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

    def test_delete_department_success(self):
        expected_message = ''
        department_id = 1

        with patch(
                'department_app.rest.department_api.DepartmentService.delete_department',
                autospec=True
        ) as delete_department_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.delete(f'/api/department/{department_id}')

            self.assertStatus(response, 204)
            self.assertEqual(expected_message, response.get_data(as_text=True))

            delete_department_mock.assert_called_once_with(department_id)
            logger_mock.debug.assert_called_once()

    def test_delete_department_failure(self):
        expected_message = 'Department not found'
        department_id = 1

        with patch(
                'department_app.rest.department_api.DepartmentService.delete_department',
                autospec=True, side_effect=ValueError
        ) as delete_department_mock, patch(
            'department_app.rest.department_api.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.delete(f'/api/department/{department_id}')

            self.assert404(response)
            self.assertEqual(expected_message, response.json)

            delete_department_mock.assert_called_once_with(department_id)
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_called_once()
