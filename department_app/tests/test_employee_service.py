# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=no-self-use, too-many-statements


from datetime import date

from unittest.mock import patch

from department_app.tests.base import BaseTestCase, SearchBaseTestCase

from department_app.service.employee_service import EmployeeService

from department_app.service.exceptions import ExistsError

from department_app.tests.data import department_1, department_2
from department_app.tests.data import employee_1, employee_2, employee_3
from department_app.tests.data import employee_to_json, employees_to_json


class TestEmployeeService(BaseTestCase):
    def test_get_employees(self):
        expected_employee = employee_to_json(employee_1)
        result = EmployeeService.get_employees()
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertIn(expected_employee, result)

        with patch(
                'department_app.service.employee_service.db.session', autospec=True
        ) as db_session_mock:
            EmployeeService.get_employees()
            db_session_mock.query.assert_called_once()

    def test_get_employee_by_id_success(self):
        expected_employee = employee_to_json(employee_1)

        employee_id = '1'
        result = EmployeeService.get_employee_by_id(employee_id)
        result = employee_to_json(result)

        self.assertEqual(expected_employee, result)

        employee_id = 1
        result = EmployeeService.get_employee_by_id(employee_id)
        result = employee_to_json(result)

        self.assertEqual(expected_employee, result)

        with patch(
                'department_app.service.employee_service.db.session', autospec=True
        ) as db_session_mock:
            EmployeeService.get_employee_by_id(employee_id)
            db_session_mock.query.assert_called_once()

    def test_get_employee_by_id_failure(self):
        result = EmployeeService.get_employee_by_id(0)
        self.assertEqual(None, result)

        self.assertRaises(TypeError, EmployeeService.get_employee_by_id, [1])
        self.assertRaises(TypeError, EmployeeService.get_employee_by_id, (1,))
        self.assertRaises(TypeError, EmployeeService.get_employee_by_id, True)

    def test_add_employee_success(self):
        expected_employee = employee_2
        expected_department = department_2
        employee_json = employee_to_json(expected_employee)

        with patch(
                'department_app.service.employee_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.employee_service.DepartmentService.get_department_by_name',
            autospec=True, return_value=expected_department
        ) as get_department_mock, patch(
            'department_app.service.employee_service.EmployeeService.schema.load',
            autospec=True, return_value=expected_employee
        ) as schema_mock:
            result = EmployeeService.add_employee(employee_json)

            get_department_mock.assert_called_once_with(employee_json['department']['name'])
            schema_mock.assert_called_once_with(employee_json)
            db_session_mock.add.assert_called_once_with(expected_employee)
            db_session_mock.commit.assert_called_once()

            self.assertEqual(expected_employee, result)

    def test_add_employee_failure(self):
        expected_employee = employee_2
        employee_json = employee_to_json(expected_employee)

        with patch(
                'department_app.service.employee_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.employee_service.DepartmentService.get_department_by_name',
            autospec=True, return_value=None
        ) as get_department_mock, patch(
            'department_app.service.employee_service.EmployeeService.schema.load',
            autospec=True, return_value=expected_employee
        ) as schema_mock:
            self.assertRaises(ExistsError, EmployeeService.add_employee, employee_json)

            get_department_mock.assert_called_once_with(employee_json['department']['name'])
            schema_mock.assert_called_once_with(employee_json)
            db_session_mock.add.assert_not_called()
            db_session_mock.commit.assert_not_called()

        employee_json['department'] = {'name': 1}

        with patch(
                'department_app.service.employee_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.employee_service.DepartmentService.get_department_by_name',
            autospec=True
        ) as get_department_mock, patch(
            'department_app.service.employee_service.EmployeeService.schema.load',
            autospec=True, return_value=expected_employee
        ) as schema_mock:
            self.assertRaises(TypeError, EmployeeService.add_employee, employee_json)

            get_department_mock.assert_not_called()
            schema_mock.assert_called_once_with(employee_json)
            db_session_mock.add.assert_not_called()
            db_session_mock.commit.assert_not_called()

    def test_update_employee_success(self):
        expected_employee = employee_1
        expected_department = department_1
        employee_id = 1
        employee_json = employee_to_json(expected_employee)

        with patch(
                'department_app.service.employee_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_name',
            autospec=True, return_value=expected_department
        ) as get_department_by_name_mock, patch(
            'department_app.service.employee_service.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_employee
        ) as get_employee_by_id_mock, patch(
            'department_app.service.employee_service.EmployeeService.schema.load',
            autospec=True, return_value=expected_employee
        ) as schema_mock:
            result = EmployeeService.update_employee(employee_id, employee_json)

            get_employee_by_id_mock.assert_called_once_with(employee_id)
            get_department_by_name_mock.assert_called_once_with(employee_json['department']['name'])
            schema_mock.assert_called_once_with(employee_json, instance=expected_employee)
            db_session_mock.add.assert_called_once_with(expected_employee)
            db_session_mock.commit.assert_called_once()

            self.assertEqual(expected_employee, result)

    def test_update_employee_failure(self):
        expected_employee = employee_1
        expected_department = department_1
        employee_id = 1
        employee_json = employee_to_json(expected_employee)

        self.assertRaises(TypeError, EmployeeService.update_employee, [1], employee_json)
        self.assertRaises(TypeError, EmployeeService.update_employee, (1,), employee_json)
        self.assertRaises(TypeError, EmployeeService.update_employee, True, employee_json)

        with patch(
                'department_app.service.employee_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_name',
            autospec=True, return_value=expected_department
        ) as get_department_by_name_mock, patch(
            'department_app.service.employee_service.EmployeeService.get_employee_by_id',
            autospec=True, return_value=None
        ) as get_employee_by_id_mock, patch(
            'department_app.service.employee_service.EmployeeService.schema.load',
            autospec=True, return_value=expected_employee
        ) as schema_mock:
            self.assertRaises(ValueError, EmployeeService.update_employee,
                              employee_id, employee_json)

            get_employee_by_id_mock.assert_called_once_with(employee_id)
            get_department_by_name_mock.assert_not_called()
            schema_mock.assert_not_called()
            db_session_mock.add.assert_not_called()
            db_session_mock.commit.assert_not_called()

        with patch(
                'department_app.service.employee_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_name',
            autospec=True, return_value=None
        ) as get_department_by_name_mock, patch(
            'department_app.service.employee_service.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_employee
        ) as get_employee_by_id_mock, patch(
            'department_app.service.employee_service.EmployeeService.schema.load',
            autospec=True, return_value=expected_employee
        ) as schema_mock:
            self.assertRaises(ExistsError, EmployeeService.update_employee,
                              employee_id, employee_json)

            get_employee_by_id_mock.assert_called_once_with(employee_id)
            get_department_by_name_mock.assert_called_once_with(employee_json['department']['name'])
            schema_mock.assert_called_once_with(employee_json, instance=expected_employee)
            db_session_mock.add.assert_not_called()
            db_session_mock.commit.assert_not_called()

        employee_json['department'] = {'name': 1}

        with patch(
                'department_app.service.employee_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_name',
            autospec=True
        ) as get_department_by_name_mock, patch(
            'department_app.service.employee_service.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_employee
        ) as get_employee_by_id_mock, patch(
            'department_app.service.employee_service.EmployeeService.schema.load',
            autospec=True, return_value=expected_employee
        ) as schema_mock:
            self.assertRaises(TypeError, EmployeeService.update_employee,
                              employee_id, employee_json)

            get_employee_by_id_mock.assert_called_once_with(employee_id)
            get_department_by_name_mock.assert_not_called()
            schema_mock.assert_called_once_with(employee_json, instance=expected_employee)
            db_session_mock.add.assert_not_called()
            db_session_mock.commit.assert_not_called()

    def test_delete_employee_success(self):
        expected_employee = employee_1
        employee_id = 1
        with patch(
                'department_app.service.employee_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.employee_service.EmployeeService.get_employee_by_id',
            autospec=True, return_value=expected_employee
        ) as get_employee_by_id_mock:
            EmployeeService.delete_employee(employee_id)

            get_employee_by_id_mock.assert_called_once_with(employee_id)
            db_session_mock.delete.assert_called_once_with(expected_employee)
            db_session_mock.commit.assert_called_once()

    def test_delete_employee_failure(self):
        self.assertRaises(TypeError, EmployeeService.delete_employee, [1])
        self.assertRaises(TypeError, EmployeeService.delete_employee, (1,))
        self.assertRaises(TypeError, EmployeeService.delete_employee, True)

        employee_id = 0
        with patch(
                'department_app.service.employee_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.employee_service.EmployeeService.get_employee_by_id',
            autospec=True, return_value=None
        ) as get_employee_by_id_mock:
            self.assertRaises(ValueError, EmployeeService.delete_employee, employee_id)

            get_employee_by_id_mock.assert_called_once_with(employee_id)
            db_session_mock.delete.assert_not_called()
            db_session_mock.commit.assert_not_called()


class TestEmployeeSearchService(SearchBaseTestCase):
    def test_get_filtered_employees_with_no_params(self):
        expected_employees = employees_to_json([employee_1, employee_2, employee_3])
        filter_params = {}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(3, len(result))
        self.assertCountEqual(expected_employees, result)

    def test_get_filtered_employees_with_one_param(self):
        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Marty'}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Maxwell'}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1, employee_3])
        filter_params = {'name': 'Ma'}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(2, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1, employee_3])
        filter_params = {'name': 'a'}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(2, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'department': 'Research'}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1, employee_2, employee_3])
        filter_params = {'department': 'ch'}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(3, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1, employee_2, employee_3])
        filter_params = {'start_salary': 0}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(3, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([])
        filter_params = {'start_salary': 5000}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(0, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1, employee_2])
        filter_params = {'start_salary': 700}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(2, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_2])
        filter_params = {'start_salary': 701}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1, employee_2, employee_3])
        filter_params = {'end_salary': 5000}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(3, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1, employee_3])
        filter_params = {'end_salary': 1000}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(2, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1, employee_3])
        filter_params = {'end_salary': 700}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(2, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_3])
        filter_params = {'end_salary': 650}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'in_date': date(2002, 5, 4)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1, employee_2])
        filter_params = {'start_date': date(2002, 5, 4)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(2, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_2])
        filter_params = {'start_date': date(2002, 5, 5)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_3])
        filter_params = {'end_date': date(2002, 5, 2)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_3, employee_1])
        filter_params = {'end_date': date(2002, 5, 4)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(2, len(result))
        self.assertCountEqual(expected_employees, result)

    def test_get_filtered_employees_with_few_params(self):
        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Marty', 'department': 'Research'}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([])
        filter_params = {'name': 'Marty', 'department': 'Purchase'}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(0, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Marty', 'start_salary': 0}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Marty', 'start_salary': 700}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([])
        filter_params = {'name': 'Marty', 'start_salary': 800}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(0, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Marty', 'end_salary': 1000}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Marty', 'end_salary': 700}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([])
        filter_params = {'name': 'Marty', 'end_salary': 100}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(0, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Marty', 'in_date': date(2002, 5, 4)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([])
        filter_params = {'name': 'Marty', 'in_date': date(2000, 5, 4)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(0, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Marty', 'start_date': date(2000, 5, 4)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Marty', 'start_date': date(2002, 5, 4)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([])
        filter_params = {'name': 'Marty', 'start_date': date(2002, 5, 5)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(0, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Marty', 'end_date': date(2002, 5, 6)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'name': 'Marty', 'end_date': date(2002, 5, 5)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([])
        filter_params = {'name': 'Marty', 'end_date': date(2002, 5, 3)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(0, len(result))
        self.assertCountEqual(expected_employees, result)

    def test_get_filtered_employees_with_range_params(self):
        expected_employees = employees_to_json([employee_1, employee_2, employee_3])
        filter_params = {'start_salary': 0, 'end_salary': 5000}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(3, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_2])
        filter_params = {'start_salary': 1000, 'end_salary': 5000}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1, employee_2])
        filter_params = {'start_salary': 500, 'end_salary': 5000}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(2, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {'start_salary': 500, 'end_salary': 2000}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        filter_params = {'start_salary': 500, 'end_salary': 100}
        self.assertRaises(ValueError, EmployeeService.get_filtered_employees, filter_params)

        expected_employees = employees_to_json([employee_1, employee_3])
        filter_params = {'start_date': date(1980, 6, 3), 'end_date': date(2002, 5, 4)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(2, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_3])
        filter_params = {'start_date': date(1980, 6, 3), 'end_date': date(2002, 5, 3)}
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        filter_params = {'start_date': date(2003, 6, 3), 'end_date': date(2002, 5, 3)}
        self.assertRaises(ValueError, EmployeeService.get_filtered_employees, filter_params)

        filter_params = {'in_date': date(2001, 10, 3),
                         'start_date': date(2001, 6, 3),
                         'end_date': date(2002, 5, 3)}
        self.assertRaises(ValueError, EmployeeService.get_filtered_employees, filter_params)

    def test_get_filtered_employees_with_all_params(self):
        expected_employees = employees_to_json([employee_1])
        filter_params = {
            'name': 'Marty',
            'department': 'Research',
            'start_salary': 100,
            'end_salary': 1000,
            'start_date': date(2001, 6, 3),
            'end_date': date(2003, 5, 3)
        }
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([employee_1])
        filter_params = {
            'name': 'Marty',
            'department': 'Research',
            'start_salary': 100,
            'end_salary': 1000,
            'in_date': date(2002, 5, 4)
        }
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(1, len(result))
        self.assertCountEqual(expected_employees, result)

        expected_employees = employees_to_json([])
        filter_params = {
            'name': 'Marty',
            'department': 'Research',
            'start_salary': 100,
            'end_salary': 1000,
            'in_date': date(2002, 5, 5)
        }
        result = EmployeeService.get_filtered_employees(filter_params)
        result = employees_to_json(result)

        self.assertEqual(0, len(result))
        self.assertCountEqual(expected_employees, result)
