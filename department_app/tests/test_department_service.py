# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, no-self-use

from unittest.mock import patch

from department_app.tests.base import BaseTestCase

from department_app.service.department_service import DepartmentService

from department_app.service.exceptions import UniqueError

from department_app.tests.data import department_1, department_2
from department_app.tests.data import department_to_json, departments_to_json


class TestDepartmentService(BaseTestCase):
    def test_get_departments(self):
        expected_department = department_to_json(department_1)
        result = DepartmentService.get_departments()
        result = departments_to_json(result)

        self.assertEqual(1, len(result))
        self.assertIn(expected_department, result)

        with patch(
                'department_app.service.department_service.db.session', autospec=True
        ) as db_session_mock:
            DepartmentService.get_departments()
            db_session_mock.query.assert_called_once()

    def test_get_department_by_id_success(self):
        expected_department = department_to_json(department_1)

        department_id = '1'
        result = DepartmentService.get_department_by_id(department_id)
        result = department_to_json(result)

        self.assertEqual(expected_department, result)

        department_id = 1
        result = DepartmentService.get_department_by_id(department_id)
        result = department_to_json(result)

        self.assertEqual(expected_department, result)

        with patch(
                'department_app.service.department_service.db.session', autospec=True
        ) as db_session_mock:
            DepartmentService.get_department_by_id(department_id)
            db_session_mock.query.assert_called_once()

    def test_get_department_by_id_failure(self):
        result = DepartmentService.get_department_by_id(0)
        self.assertEqual(None, result)

        self.assertRaises(TypeError, DepartmentService.get_department_by_id, [1])
        self.assertRaises(TypeError, DepartmentService.get_department_by_id, (1,))
        self.assertRaises(TypeError, DepartmentService.get_department_by_id, True)

    def test_get_department_by_name_success(self):
        expected_department = department_to_json(department_1)
        department_name = department_1.name
        result = DepartmentService.get_department_by_name(department_name)
        result = department_to_json(result)

        self.assertEqual(expected_department, result)

        with patch(
                'department_app.service.department_service.db.session', autospec=True
        ) as db_session_mock:
            DepartmentService.get_department_by_name(department_name)
            db_session_mock.query.assert_called_once()

    def test_get_department_by_name_failure(self):
        result = DepartmentService.get_department_by_name('no_name')
        self.assertEqual(None, result)

        self.assertRaises(TypeError, DepartmentService.get_department_by_name, 1)
        self.assertRaises(TypeError, DepartmentService.get_department_by_name, True)

    def test_add_department_success(self):
        expected_department = department_2
        department_json = department_to_json(expected_department)

        with patch(
                'department_app.service.department_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_name',
            autospec=True, return_value=None
        ) as get_department_mock, patch(
            'department_app.service.department_service.DepartmentService.schema.load',
            autospec=True, return_value=expected_department
        ) as schema_mock:
            result = DepartmentService.add_department(department_json)

            get_department_mock.assert_called_once_with(department_json['name'])
            schema_mock.assert_called_once_with(department_json)
            db_session_mock.add.assert_called_once_with(expected_department)
            db_session_mock.commit.assert_called_once()

            self.assertEqual(expected_department, result)

    def test_add_department_failure(self):
        expected_department = department_1
        department_json = department_to_json(expected_department)

        with patch(
                'department_app.service.department_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_name',
            autospec=True, return_value=(department_json.get('name', None))
        ) as get_department_by_name_mock, patch(
            'department_app.service.department_service.DepartmentService.schema.load',
            autospec=True, return_value=expected_department
        ) as schema_mock:
            self.assertRaises(UniqueError, DepartmentService.add_department, department_json)

            get_department_by_name_mock.assert_called_once_with(department_json.get('name', None))
            schema_mock.assert_not_called()
            db_session_mock.add.assert_not_called()
            db_session_mock.commit.assert_not_called()

        department_json = {'name': 15}
        self.assertRaises(TypeError, DepartmentService.add_department, department_json)

    def test_update_department_success(self):
        expected_department = department_1
        department_id = 1
        department_json = department_to_json(expected_department)

        with patch(
                'department_app.service.department_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_name',
            autospec=True, return_value=expected_department
        ) as get_department_by_name_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_id',
            autospec=True, return_value=expected_department
        ) as get_department_by_id_mock, patch(
            'department_app.service.department_service.DepartmentService.schema.load',
            autospec=True, return_value=expected_department
        ) as schema_mock:
            result = DepartmentService.update_department(department_id, department_json)

            get_department_by_id_mock.assert_called_once_with(department_id)
            get_department_by_name_mock.assert_called_once_with(department_json['name'])
            schema_mock.assert_called_once_with(department_json, instance=expected_department)
            db_session_mock.add.assert_called_once_with(expected_department)
            db_session_mock.commit.assert_called_once()

            self.assertEqual(expected_department, result)

    def test_update_department_failure(self):
        expected_department = department_1
        department_id = 0
        department_json = department_to_json(expected_department)

        self.assertRaises(TypeError, DepartmentService.update_department, [1, ], department_json)
        self.assertRaises(TypeError, DepartmentService.update_department, True, department_json)

        with patch(
                'department_app.service.department_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_name',
            autospec=True, return_value=expected_department
        ) as get_department_by_name_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_id',
            autospec=True, return_value=None
        ) as get_department_by_id_mock, patch(
            'department_app.service.department_service.DepartmentService.schema.load',
            autospec=True, return_value=expected_department
        ) as schema_mock:
            self.assertRaises(ValueError, DepartmentService.update_department,
                              department_id, department_json)

            get_department_by_id_mock.assert_called_once_with(department_id)
            get_department_by_name_mock.assert_not_called()
            schema_mock.assert_not_called()
            db_session_mock.add.assert_not_called()
            db_session_mock.commit.assert_not_called()

        with patch(
                'department_app.service.department_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_name',
            autospec=True, return_value={'name': 'random'}
        ) as get_department_by_name_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_id',
            autospec=True, return_value=expected_department
        ) as get_department_by_id_mock, patch(
            'department_app.service.department_service.DepartmentService.schema.load',
            autospec=True, return_value=expected_department
        ) as schema_mock:
            self.assertRaises(UniqueError, DepartmentService.update_department,
                              department_id, department_json)

            get_department_by_id_mock.assert_called_once_with(department_id)
            get_department_by_name_mock.assert_called_once_with(department_json['name'])
            schema_mock.assert_not_called()
            db_session_mock.add.assert_not_called()
            db_session_mock.commit.assert_not_called()

        department_json = {'name': 15}
        self.assertRaises(TypeError, DepartmentService.update_department,
                          1, department_json)

    def test_delete_department_success(self):
        expected_department = department_1
        department_id = 1
        with patch(
                'department_app.service.department_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_id',
            autospec=True, return_value=expected_department
        ) as get_department_by_id_mock:
            DepartmentService.delete_department(department_id)

            get_department_by_id_mock.assert_called_once_with(department_id)
            db_session_mock.delete.assert_called_once_with(expected_department)
            db_session_mock.commit.assert_called_once()

    def test_delete_department_failure(self):
        self.assertRaises(TypeError, DepartmentService.delete_department, [1, ])
        self.assertRaises(TypeError, DepartmentService.delete_department, True)

        department_id = 0
        with patch(
                'department_app.service.department_service.db.session', autospec=True
        ) as db_session_mock, patch(
            'department_app.service.department_service.DepartmentService.get_department_by_id',
            autospec=True, return_value=None
        ) as get_department_by_id_mock:
            self.assertRaises(ValueError, DepartmentService.delete_department, department_id)

            get_department_by_id_mock.assert_called_once_with(department_id)
            db_session_mock.delete.assert_not_called()
            db_session_mock.commit.assert_not_called()
