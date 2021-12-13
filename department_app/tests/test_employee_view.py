# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import json
from unittest.mock import patch

from datetime import date

from department_app.tests.base import BaseTestCase

from department_app.tests.data import department_1
from department_app.tests.data import department_to_json

from department_app.tests.data import employee_1
from department_app.tests.data import employee_to_json, employees_to_json


class TestEmployeeView(BaseTestCase):
    def test_get_employees_success(self):
        expected_employees = [employee_1]
        expected_json = employees_to_json(expected_employees, with_id=True)

        form_data = {
            'name': None,
            'department': None,
            'start_salary': None,
            'end_salary': None,
            'date_input_type': 'in',
            'start_date': None,
            'end_date': None,
            'submit': False
        }

        form_input = {
            'name': '',
            'department': '',
            'start_salary': '',
            'end_salary': '',
            'date_input_type': 'in',
            'start_date': '',
            'end_date': '',
            'submit': False
        }

        with patch(
                'department_app.views.employee_view.EmployeeService.get_employees',
                autospec=True, return_value=expected_employees
        ) as get_employees_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_filtered_employees',
            autospec=True, return_value=expected_employees
        ) as get_filtered_employees_mock, patch(
            'department_app.views.employee_view.employees_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get('/employees/')

            self.assert200(response)
            self.assertTemplateUsed('employees.html')
            self.assertContext('employees', expected_json)
            self.assertContext('prev_input', form_data)

            get_employees_mock.assert_called_once()
            get_filtered_employees_mock.assert_not_called()
            schema_mock.assert_called_once_with(expected_employees)
            logger_mock.debug.assert_called()

        form_data = {
            'name': '',
            'department': '',
            'start_salary': None,
            'end_salary': None,
            'date_input_type': 'in',
            'start_date': None,
            'end_date': None,
        }

        filter_data = {
            'name': '',
            'department': '',
            'start_salary': None,
            'end_salary': None,
            'start_date': None,
            'end_date': None,
            'in_date': None
        }

        filter_data['name'] = form_data['name'] = form_input['name'] = 'test name'
        form_data['submit'] = False

        with patch(
                'department_app.views.employee_view.EmployeeService.get_employees',
                autospec=True, return_value=expected_employees
        ) as get_employees_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_filtered_employees',
            autospec=True, return_value=expected_employees
        ) as get_filtered_employees_mock, patch(
            'department_app.views.employee_view.employees_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/employees/',
                                        data=json.dumps(form_input),
                                        content_type='application/json')

            self.assert200(response)
            self.assertTemplateUsed('employees.html')
            self.assertContext('employees', expected_json)
            self.assertContext('prev_input', form_data)

            get_employees_mock.assert_called_once()
            get_filtered_employees_mock.assert_called_once_with(filter_data)
            schema_mock.assert_called_once_with(expected_employees)
            logger_mock.debug.assert_called()

        filter_data['name'] = form_data['name'] = form_input['name'] = 'test name'
        form_data['date_input_type'] = form_input['date_input_type'] = 'between'
        form_data['submit'] = False

        with patch(
                'department_app.views.employee_view.EmployeeService.get_employees',
                autospec=True, return_value=expected_employees
        ) as get_employees_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_filtered_employees',
            autospec=True, return_value=expected_employees
        ) as get_filtered_employees_mock, patch(
            'department_app.views.employee_view.employees_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/employees/',
                                        data=json.dumps(form_input),
                                        content_type='application/json')

            self.assert200(response)
            self.assertTemplateUsed('employees.html')
            self.assertContext('employees', expected_json)
            self.assertContext('prev_input', form_data)

            get_employees_mock.assert_called_once()
            get_filtered_employees_mock.assert_called_once_with(filter_data)
            schema_mock.assert_called_once_with(expected_employees)
            logger_mock.debug.assert_called()

    def test_get_employees_failure(self):
        expected_employees = [employee_1]
        expected_json = employees_to_json(expected_employees, with_id=True)

        form_input = {
            'name': '',
            'department': '',
            'start_salary': '',
            'end_salary': '',
            'date_input_type': 'in',
            'start_date': '',
            'end_date': '',
            'submit': False
        }

        form_data = {
            'name': '',
            'department': '',
            'start_salary': None,
            'end_salary': None,
            'date_input_type': 'in',
            'start_date': None,
            'end_date': None,
        }

        filter_data = {
            'name': '',
            'department': '',
            'start_salary': None,
            'end_salary': None,
            'start_date': None,
            'end_date': None,
            'in_date': None
        }

        filter_data['start_salary'] = form_data['start_salary'] = form_input['start_salary'] = 2000
        filter_data['end_salary'] = form_data['end_salary'] = form_input['end_salary'] = 1000
        form_data['submit'] = False

        with patch(
                'department_app.views.employee_view.EmployeeService.get_employees',
                autospec=True, return_value=expected_employees
        ) as get_employees_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_filtered_employees',
            autospec=True
        ) as get_filtered_employees_mock, patch(
            'department_app.views.employee_view.employees_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/employees/',
                                        data=json.dumps(form_input),
                                        content_type='application/json')

            self.assert200(response)
            self.assertTemplateUsed('employees.html')
            self.assertContext('employees', expected_json)
            self.assertContext('prev_input', form_data)

            self.assertMessageFlashed('To:end salary must be less than start salary'
                                      , category='danger')

            get_employees_mock.assert_called_once()
            get_filtered_employees_mock.assert_not_called()
            schema_mock.assert_called_once_with(expected_employees)
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

    def test_get_employee_success(self):
        expected_employee = employee_1
        employee_id = 1
        expected_json = employee_to_json(expected_employee, with_id=True)

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True
        ) as get_department_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_employee
        ) as get_employee_mock, patch(
            'department_app.views.employee_view.employee_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/employees/{employee_id}')

            self.assert200(response)
            self.assertTemplateUsed('employee.html')
            self.assertContext('employee', expected_json)
            self.assertContext('department_id', None)
            self.assertContext('from_department', False)

            get_department_mock.assert_not_called()
            get_employee_mock.assert_called_once_with(employee_id)
            schema_mock.assert_called_once_with(expected_employee)
            logger_mock.debug.assert_called()

        department_id = 1
        expected_department = department_1

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_employee
        ) as get_employee_mock, patch(
            'department_app.views.employee_view.employee_schema.dump',
            autospec=True, return_value=expected_json
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}/employees/{employee_id}')

            self.assert200(response)
            self.assertTemplateUsed('employee.html')
            self.assertContext('employee', expected_json)
            self.assertContext('department_id', department_id)
            self.assertContext('from_department', True)

            get_department_mock.assert_called_once_with(department_id)
            get_employee_mock.assert_called_once_with(employee_id)
            schema_mock.assert_called_once_with(expected_employee)
            logger_mock.debug.assert_called()

    def test_get_employee_failure(self):
        employee_id = 1

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True
        ) as get_department_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True, return_value=None
        ) as get_employee_mock, patch(
            'department_app.views.employee_view.employee_schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/employees/{employee_id}')

            self.assert200(response)
            self.assertTemplateUsed('empty.html')

            get_department_mock.assert_not_called()
            get_employee_mock.assert_called_once_with(employee_id)
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

        department_id = 1

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=None
        ) as get_department_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True
        ) as get_employee_mock, patch(
            'department_app.views.employee_view.employee_schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}/employees/{employee_id}')

            self.assert200(response)
            self.assertTemplateUsed('empty.html')

            get_department_mock.assert_called_once_with(department_id)
            get_employee_mock.assert_not_called()
            schema_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

    def test_add_employee_get_success(self):
        form_data = {
            'name': None,
            'department': None,
            'salary': None,
            'date_of_birth': None,
            'submit': False
        }

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True
        ) as get_department_mock, patch(
            'department_app.views.employee_view.EmployeeService.add_employee',
            autospec=True
        ) as add_employee_mock, patch(
            'department_app.views.employee_view.department_schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get('/employees/new')

            self.assertStatus(response, 200)
            self.assertTemplateUsed('employee_form.html')
            self.assertContext('employee', {})
            self.assertContext('department', {})
            self.assertContext('new', True)
            self.assertContext('from_department', False)
            self.assertContext('prev_input', form_data)

            get_department_mock.assert_not_called()
            schema_mock.assert_not_called()
            add_employee_mock.assert_not_called()
            logger_mock.debug.assert_called_once()

        department_id = 1
        expected_department = department_1
        expected_department_json = department_to_json(expected_department,
                                                      with_id=True, nested=True)
        del form_data['department']

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_mock, patch(
            'department_app.views.employee_view.EmployeeService.add_employee',
            autospec=True
        ) as add_employee_mock, patch(
            'department_app.views.employee_view.department_schema.dump',
            autospec=True, return_value=expected_department_json
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}/employees/new')

            self.assertStatus(response, 200)
            self.assertTemplateUsed('employee_form.html')
            self.assertContext('employee', {})
            self.assertContext('department', expected_department_json)
            self.assertContext('new', True)
            self.assertContext('from_department', True)
            self.assertContext('prev_input', form_data)

            get_department_mock.assert_called_once_with(department_id)
            schema_mock.assert_called_once_with(expected_department)
            add_employee_mock.assert_not_called()
            logger_mock.debug.assert_called()

    def test_add_employee_get_failure(self):
        department_id = 5

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=None
        ) as get_department_mock, patch(
            'department_app.views.employee_view.EmployeeService.add_employee',
            autospec=True
        ) as add_employee_mock, patch(
            'department_app.views.employee_view.department_schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}/employees/new')

            self.assertStatus(response, 200)
            self.assertTemplateUsed('empty.html')

            get_department_mock.assert_called_once_with(department_id)
            schema_mock.assert_not_called()
            add_employee_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

    def test_add_employee_post_success(self):
        expected_employee = employee_1
        expected_employee_json = employee_to_json(expected_employee, nested=True)
        expected_employee_json['department'] = {'name': department_1.name}
        data = expected_employee_json.copy()
        data['department'] = department_1.name
        data['date_of_birth'] = '2002-05-04'

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True
        ) as get_department_mock, patch(
            'department_app.views.employee_view.EmployeeService.add_employee',
            autospec=True
        ) as add_employee_mock, patch(
            'department_app.views.employee_view.department_schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/employees/new',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert_redirects(response, '/employees/')
            self.assert_message_flashed('Employee has been created successfully',
                                        category='success')

            get_department_mock.assert_not_called()
            schema_mock.assert_not_called()
            add_employee_mock.assert_called_once_with(expected_employee_json)
            logger_mock.debug.assert_called()

        department_id = 1
        expected_department = department_1
        expected_department_json = department_to_json(expected_department,
                                                      with_id=True, nested=True)

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_mock, patch(
            'department_app.views.employee_view.EmployeeService.add_employee',
            autospec=True, return_value=expected_department_json
        ) as add_employee_mock, patch(
            'department_app.views.employee_view.department_schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post(f'/departments/{department_id}/employees/new',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert_redirects(response, f'/departments/{department_id}')
            self.assert_message_flashed('Employee has been created successfully',
                                        category='success')

            get_department_mock.assert_called_once_with(department_id)
            schema_mock.assert_called_once_with(expected_department)

            expected_employee_json['department']['name'] = schema_mock(expected_department)['name']
            add_employee_mock.assert_called_once_with(expected_employee_json)

            logger_mock.debug.assert_called()

    def test_add_employee_post_failure(self):
        expected_employee = employee_1
        expected_employee_json = employee_to_json(expected_employee, nested=True)
        expected_employee_json['department'] = {'name': 'no department'}
        data = expected_employee_json.copy()
        data['department'] = 'no department'
        data['date_of_birth'] = '2002-05-04'
        form_data = data.copy()
        form_data['date_of_birth'] = date(2002, 5, 4)
        form_data['submit'] = False

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True
        ) as get_department_mock, patch(
            'department_app.views.employee_view.EmployeeService.add_employee',
            autospec=True
        ) as add_employee_mock, patch(
            'department_app.views.employee_view.department_schema.dump', autospec=True
        ) as schema_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post('/employees/new',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assertStatus(response, 200)
            self.assertTemplateUsed('employee_form.html')
            self.assertContext('employee', {})
            self.assertContext('department', {})
            self.assertContext('new', True)
            self.assertContext('from_department', False)
            self.assertContext('prev_input', form_data)
            self.assert_message_flashed(r"Department: Department with such name doesn't exist",
                                        category='danger')

            get_department_mock.assert_not_called()
            schema_mock.assert_not_called()
            add_employee_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

    def test_edit_employee_get_success(self):
        employee_id = 1
        expected_employee = employee_1
        expected_employee_json = employee_to_json(expected_employee, with_id=True)
        form_data = {
            'name': None,
            'department': None,
            'salary': None,
            'date_of_birth': None,
            'submit': False
        }

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True
        ) as get_department_by_id_mock, patch(
            'department_app.views.employee_view.department_schema.dump', autospec=True
        ) as department_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_employee
        ) as get_employee_by_id_mock, patch(
            'department_app.views.employee_view.employee_schema.dump',
            autospec=True, return_value=expected_employee_json
        ) as employee_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.update_employee',
            autospec=True
        ) as update_employee_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/employees/{employee_id}/edit')

            self.assert200(response)
            self.assertTemplateUsed('employee_form.html')
            self.assertContext('employee', expected_employee_json)
            self.assertContext('department', {})
            self.assertContext('new', False)
            self.assertContext('from_department', False)
            self.assertContext('prev_input', form_data)

            get_department_by_id_mock.assert_not_called()
            department_schema_mock.assert_not_called()
            get_employee_by_id_mock.assert_called_once_with(employee_id)
            employee_schema_mock.assert_called_once_with(expected_employee)
            update_employee_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_not_called()

        department_id = 1
        expected_department = department_1
        expected_department_json = department_to_json(expected_department,
                                                      with_id=True, nested=True)
        del form_data['department']

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_by_id_mock, patch(
            'department_app.views.employee_view.department_schema.dump',
            autospec=True, return_value=expected_department_json
        ) as department_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_employee
        ) as get_employee_by_id_mock, patch(
            'department_app.views.employee_view.employee_schema.dump',
            autospec=True, return_value=expected_employee_json
        ) as employee_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.update_employee',
            autospec=True
        ) as update_employee_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}/employees/{employee_id}/edit')

            self.assert200(response)
            self.assertTemplateUsed('employee_form.html')
            self.assertContext('employee', expected_employee_json)
            self.assertContext('department', expected_department_json)
            self.assertContext('new', False)
            self.assertContext('from_department', True)
            self.assertContext('prev_input', form_data)

            get_department_by_id_mock.assert_called_once_with(department_id)
            department_schema_mock.assert_called_once_with(expected_department)
            get_employee_by_id_mock.assert_called_once_with(employee_id)
            employee_schema_mock.assert_called_once_with(expected_employee)
            update_employee_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_not_called()

    def test_edit_employee_get_failure(self):
        employee_id = 5

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True
        ) as get_department_by_id_mock, patch(
            'department_app.views.employee_view.department_schema.dump', autospec=True
        ) as department_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True, return_value=None
        ) as get_employee_by_id_mock, patch(
            'department_app.views.employee_view.employee_schema.dump', autospec=True
        ) as employee_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.update_employee',
            autospec=True
        ) as update_employee_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/employees/{employee_id}/edit')

            self.assert200(response)
            self.assertTemplateUsed('empty.html')

            get_department_by_id_mock.assert_not_called()
            department_schema_mock.assert_not_called()
            get_employee_by_id_mock.assert_called_once_with(employee_id)
            employee_schema_mock.assert_not_called()
            update_employee_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

        department_id = 5
        expected_employee = employee_1

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=None
        ) as get_department_by_id_mock, patch(
            'department_app.views.employee_view.department_schema.dump'
            , autospec=True
        ) as department_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_employee
        ) as get_employee_by_id_mock, patch(
            'department_app.views.employee_view.employee_schema.dump', autospec=True
        ) as employee_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.update_employee',
            autospec=True
        ) as update_employee_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/departments/{department_id}/employees/{employee_id}/edit')

            self.assert200(response)
            self.assertTemplateUsed('empty.html')

            get_department_by_id_mock.assert_called_once_with(department_id)
            department_schema_mock.assert_not_called()
            get_employee_by_id_mock.assert_called_once_with(employee_id)
            employee_schema_mock.assert_called_once_with(expected_employee)
            update_employee_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

    def test_edit_employee_post_success(self):
        employee_id = 1
        expected_employee = employee_1
        expected_employee_json = employee_to_json(expected_employee, nested=True, with_id=True)
        expected_employee_json['department'] = {'name': department_1.name}
        data = expected_employee_json.copy()
        data['department'] = department_1.name
        data['date_of_birth'] = '2002-05-04'
        del data['id']

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True
        ) as get_department_by_id_mock, patch(
            'department_app.views.employee_view.department_schema.dump', autospec=True
        ) as department_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_employee
        ) as get_employee_by_id_mock, patch(
            'department_app.views.employee_view.employee_schema.dump',
            autospec=True, return_value=expected_employee_json
        ) as employee_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.update_employee',
            autospec=True
        ) as update_employee_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post(f'/employees/{employee_id}/edit',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assert_redirects(response, f'/employees/{employee_id}')
            self.assert_message_flashed('Employee has been updated successfully',
                                        category='success')

            get_department_by_id_mock.assert_not_called()
            department_schema_mock.assert_not_called()
            get_employee_by_id_mock.assert_called_once_with(employee_id)
            employee_schema_mock.assert_called_once_with(expected_employee)

            del expected_employee_json['id']
            update_employee_mock.assert_called_once_with(employee_id, expected_employee_json)

            logger_mock.debug.assert_called()
            logger_mock.error.assert_not_called()

        expected_employee_json['id'] = employee_id
        department_id = 1
        expected_department = department_1
        expected_department_json = department_to_json(expected_department,
                                                      with_id=True, nested=True)

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=expected_department
        ) as get_department_by_id_mock, patch(
            'department_app.views.employee_view.department_schema.dump',
            autospec=True, return_value=expected_department_json
        ) as department_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_employee
        ) as get_employee_by_id_mock, patch(
            'department_app.views.employee_view.employee_schema.dump',
            autospec=True, return_value=expected_employee_json
        ) as employee_schema_mock, patch(
            'department_app.views.employee_view.EmployeeService.update_employee',
            autospec=True
        ) as update_employee_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.post(
                f'/departments/{department_id}/employees/{employee_id}/edit',
                data=json.dumps(data),
                content_type='application/json'
            )

            self.assert_redirects(response,
                                  f'/departments/{department_id}/employees/{employee_id}')
            self.assert_message_flashed('Employee has been updated successfully',
                                        category='success')

            get_department_by_id_mock.assert_called_once_with(department_id)
            department_schema_mock.assert_called_once_with(expected_department)
            get_employee_by_id_mock.assert_called_once_with(employee_id)
            employee_schema_mock.assert_called_once_with(expected_employee)

            del expected_employee_json['id']
            update_employee_mock.assert_called_once_with(employee_id, expected_employee_json)

            logger_mock.debug.assert_called()
            logger_mock.error.assert_not_called()

    def test_delete_employee_success(self):
        employee_id = 1
        expected_employee = employee_1

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True
        ) as get_department_by_id_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True
        ) as get_employee_by_id_mock, patch(
            'department_app.views.employee_view.EmployeeService.delete_employee',
            autospec=True, return_value=expected_employee
        ) as delete_employee_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/employees/{employee_id}/delete')

            self.assert_redirects(response, '/employees/')
            self.assert_message_flashed('Employee has been deleted successfully',
                                        category='success')

            get_department_by_id_mock.assert_not_called()
            get_employee_by_id_mock.assert_called_once_with(employee_id)
            delete_employee_mock.assert_called_once_with(employee_id)
            logger_mock.debug.assert_not_called()
            logger_mock.error.assert_not_called()

        department_id = 1
        expected_department = department_1

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True
        ) as get_department_by_id_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_department
        ) as get_employee_by_id_mock, patch(
            'department_app.views.employee_view.EmployeeService.delete_employee',
            autospec=True, return_value=expected_employee
        ) as delete_employee_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(
                f'/departments/{department_id}/employees/{employee_id}/delete')

            self.assert_redirects(response, f'/departments/{department_id}/edit')
            self.assert_message_flashed('Employee has been deleted successfully',
                                        category='success')

            get_department_by_id_mock.assert_called_once_with(department_id)
            get_employee_by_id_mock.assert_called_once_with(employee_id)
            delete_employee_mock.assert_called_once_with(employee_id)
            logger_mock.debug.assert_called()
            logger_mock.error.assert_not_called()

    def test_delete_employee_failure(self):
        employee_id = 5

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True
        ) as get_department_by_id_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True, return_value=None
        ) as get_employee_by_id_mock, patch(
            'department_app.views.employee_view.EmployeeService.delete_employee',
            autospec=True
        ) as delete_employee_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(f'/employees/{employee_id}/delete')

            self.assert200(response)
            self.assertTemplateUsed('empty.html')

            get_department_by_id_mock.assert_not_called()
            get_employee_by_id_mock.assert_called_once_with(employee_id)
            delete_employee_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()

        department_id = 5

        with patch(
                'department_app.views.employee_view.DepartmentService.get_department_by_id',
                autospec=True, return_value=None
        ) as get_department_by_id_mock, patch(
            'department_app.views.employee_view.EmployeeService.get_employee_by_id',
            autospec=True
        ) as get_employee_by_id_mock, patch(
            'department_app.views.employee_view.EmployeeService.delete_employee',
            autospec=True
        ) as delete_employee_mock, patch(
            'department_app.views.employee_view.app.logger', autospec=True
        ) as logger_mock:
            response = self.client.get(
                f'/departments/{department_id}/employees/{employee_id}/delete')

            self.assert200(response)
            self.assertTemplateUsed('empty.html')

            get_department_by_id_mock.assert_called_once_with(department_id)
            get_employee_by_id_mock.assert_not_called()
            delete_employee_mock.assert_not_called()
            logger_mock.debug.assert_called()
            logger_mock.error.assert_called_once()
