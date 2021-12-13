# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import json
from unittest.mock import patch

from department_app.tests.base import BaseTestCase

from department_app.tests.data import department_1
from department_app.tests.data import department_to_json, departments_to_json


class TestDepartmentView(BaseTestCase):
    def test_get_departments(self):
        expected_departments = [department_1]
        expected_json = departments_to_json(expected_departments, with_id=True)

        with patch(
                'department_app.views.department_view.DepartmentService.get_departments',
                autospec=True, return_value=expected_departments
        ) as get_departments_mock, patch(
            'department_app.views.department_view.departments_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get('/')

            self.assert200(response)
            self.assertTemplateUsed('departments.html')
            self.assertContext('departments', expected_json)

            get_departments_mock.assert_called_once()
            schema_mock.assert_called_once_with(expected_departments)
            logger_mock.debug.assert_called()

        with patch(
                'department_app.views.department_view.DepartmentService.get_departments',
                autospec=True, return_value=expected_departments
        ) as get_departments_mock, patch(
            'department_app.views.department_view.departments_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get('/departments/')

            self.assert200(response)
            self.assertTemplateUsed('departments.html')
            self.assertContext('departments', expected_json)

            get_departments_mock.assert_called_once()
            schema_mock.assert_called_once_with(expected_departments)
            logger_mock.debug.assert_called()

    def test_get_department_success(self):
        expected_department = department_1
        department_id = 1
        expected_json = department_to_json(expected_department, with_id=True)

        with patch(
                'department_app.views.department_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_mock, patch(
            'department_app.views.department_view.department_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}')

            self.assert200(response)
            self.assertTemplateUsed('department.html')
            self.assertContext('department', expected_json)

            get_department_mock.assert_called_once_with(department_id)
            schema_mock.assert_called_once_with(expected_department)
            logger_mock.debug.assert_called()

    def test_get_department_failure(self):
        department_id = 0

        with patch(
                'department_app.views.department_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=None
        ) as get_department_mock, patch(
            'department_app.views.department_view.department_schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}', follow_redirects=True)

            self.assert200(response)
            self.assertTemplateUsed('empty.html')

            get_department_mock.assert_called_once_with(department_id)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

    def test_add_department_get(self):
        form_data = {'name': None, 'submit': False}

        with patch(
                'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get('/departments/new')

            self.assert200(response)
            self.assertTemplateUsed('department_form.html')
            self.assertContext('department', {})
            self.assertContext('new', True)
            self.assertContext('prev_input', form_data)

            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_not_called()

    def test_add_department_post_success(self):
        data = expected_json = {'name': 'Test name'}
        form_data = expected_json.copy()
        form_data['submit'] = True

        with patch(
                'department_app.views.department_view.DepartmentService.add_department',
                autospec=True
        ) as service_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/departments/new',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert_redirects(response, '/departments/')
            self.assert_message_flashed('Department has been created successfully',
                                        category='success')

            service_mock.assert_called_once_with(expected_json)
            logger_mock.debug.assert_called_once()
            logger_mock.error.assert_not_called()

    def test_add_department_post_failure(self):
        data = expected_json = {'name': department_1.name}
        form_data = expected_json.copy()
        form_data['submit'] = False

        with patch(
                'department_app.views.department_view.DepartmentService.add_department',
                autospec=True
        ) as service_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/departments/new',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert200(response)
            self.assertTemplateUsed('department_form.html')
            self.assertContext('department', {})
            self.assertContext('new', True)
            self.assertContext('prev_input', form_data)
            self.assert_message_flashed('Name: Department with such name already exists',
                                        category='danger')

            service_mock.assert_not_called()
            logger_mock.assert_not_called()
            logger_mock.error.assert_called_once()

    def test_edit_department_get_success(self):
        department_id = 1
        expected_department = department_1
        expected_json = department_to_json(expected_department, with_id=True)
        form_data = {'name': None, 'submit': False}

        with patch(
                'department_app.views.department_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_by_id_mock, patch(
            'department_app.views.department_view.department_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}/edit')

            self.assert200(response)
            self.assertTemplateUsed('department_form.html')
            self.assertContext('department', expected_json)
            self.assertContext('new', False)
            self.assertContext('prev_input', form_data)

            get_department_by_id_mock.assert_called_once_with(department_id)
            schema_mock.assert_called_once_with(expected_department)
            logger_mock.debug.assert_called()
            logger_mock.error.assert_not_called()

    def test_edit_department_get_failure(self):
        department_id = 0

        with patch(
                'department_app.views.department_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=None
        ) as get_department_by_id_mock, patch(
            'department_app.views.department_view.department_schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}/edit')

            self.assert200(response)
            self.assertTemplateUsed('empty.html')

            get_department_by_id_mock.assert_called_once_with(department_id)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

    def test_edit_department_post_success(self):
        department_id = 1
        expected_department = department_1
        expected_json = department_to_json(expected_department, with_id=True)
        data = {'name': 'Test name'}
        form_data = data.copy()
        form_data['submit'] = True

        with patch(
                'department_app.views.department_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_by_id_mock, patch(
            'department_app.views.department_view.DepartmentService.update_department',
            autospec=True, return_value=expected_department
        ) as update_department_mock, patch(
            'department_app.views.department_view.department_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post(f'/departments/{department_id}/edit',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert_redirects(response, f'/departments/{department_id}')
            self.assert_message_flashed('Department has been updated successfully',
                                        category='success')

            get_department_by_id_mock.assert_called_once_with(department_id)
            update_department_mock.assert_called_once_with(department_id, data)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_not_called()

        data = {'name': expected_department.name}
        form_data = data.copy()
        form_data['submit'] = True

        with patch(
                'department_app.views.department_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_by_id_mock, patch(
            'department_app.views.department_view.DepartmentService.get_department_by_name',
            autospec=True, return_value=expected_department
        ) as get_department_by_name_mock, patch(
            'department_app.views.department_view.DepartmentService.update_department',
            autospec=True, return_value=expected_department
        ) as update_department_mock, patch(
            'department_app.views.department_view.department_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post(f'/departments/{department_id}/edit',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert_redirects(response, f'/departments/{department_id}')
            self.assert_message_flashed('Department has been updated successfully',
                                        category='success')

            get_department_by_id_mock.assert_called_once_with(department_id)
            get_department_by_name_mock.assert_called_once_with(expected_department.name)
            update_department_mock.assert_not_called()
            schema_mock.assert_not_called()
            logger_mock.debug.assert_not_called()
            logger_mock.error.assert_not_called()

    def test_edit_department_post_failure(self):
        department_id = 1
        expected_department = department_1
        expected_json = department_to_json(expected_department, with_id=True)
        data = {'name': 'Research'}
        form_data = data.copy()
        form_data['submit'] = False

        with patch(
                'department_app.views.department_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_by_id_mock, patch(
            'department_app.views.department_view.DepartmentService.update_department',
            autospec=True
        ) as update_department_mock, patch(
            'department_app.views.department_view.department_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post(f'/departments/{department_id}/edit',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert200(response)
            self.assertTemplateUsed('department_form.html')
            self.assertContext('department', expected_json)
            self.assertContext('new', False)
            self.assertContext('prev_input', form_data)
            self.assert_message_flashed('Name: Department with such name already exists',
                                        category='danger')

            get_department_by_id_mock.assert_called_once_with(department_id)
            update_department_mock.assert_not_called()
            schema_mock.assert_called_once_with(expected_department)
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

    def test_delete_department_success(self):
        department_id = 1
        expected_department = department_1

        with patch(
                'department_app.views.department_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_by_id_mock, patch(
            'department_app.views.department_view.DepartmentService.delete_department',
            autospec=True
        ) as delete_department_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}/delete')

            self.assert_redirects(response, '/departments/')
            self.assert_message_flashed('Department has been deleted successfully',
                                        category='success')

            get_department_by_id_mock.assert_called_once_with(department_id)
            delete_department_mock.assert_called_once_with(department_id)
            logger_mock.debug.assert_not_called()
            logger_mock.error.assert_not_called()

    def test_delete_department_failure(self):
        department_id = 0

        with patch(
                'department_app.views.department_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=None
        ) as get_department_by_id_mock, patch(
            'department_app.views.department_view.DepartmentService.delete_department',
            autospec=True
        ) as delete_department_mock, patch(
            'department_app.views.department_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}/delete')

            self.assert200(response)
            self.assertTemplateUsed('empty.html')

            get_department_by_id_mock.assert_called_once_with(department_id)
            delete_department_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()
