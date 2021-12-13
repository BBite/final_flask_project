# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from datetime import date

from department_app.models.department import Department
from department_app.models.employee import Employee

department_1 = Department('Research')
department_2 = Department('Purchase')

employee_1 = Employee('Marty Maxwell', 700, date(2002, 5, 4), department_1)
employee_2 = Employee('Erin Dolton', 4000, date(2002, 6, 3), department_2)
employee_3 = Employee('Alex Marshman', 250, date(1989, 11, 30), department_2)


def employee_to_json(employee, nested=False, with_id=False):
    result = {
        'name': employee.name,
        'salary': employee.salary,
        'date_of_birth': employee.date_of_birth.strftime('%d.%m.%Y')
    }

    if not nested:
        result['department'] = department_to_json(
            employee.department, nested=True, with_id=with_id
        )

    if with_id:
        result['id'] = 1

    return result


def department_to_json(department, nested=False, with_id=False):
    total_salary = sum([employee.salary for employee in department.employees])
    result = {
        'name': department.name,
        'avg_salary': (total_salary / len(department.employees)
                       if len(department.employees) else 0)
    }

    if not nested:
        result['employees'] = [
            employee_to_json(e, nested=True, with_id=with_id) for e in department.employees
        ]

    if with_id:
        result['id'] = 1

    return result


def departments_to_json(departments, with_id=False):
    return list(map(lambda department: department_to_json(department, with_id=with_id),
                    departments))


def employees_to_json(employees, with_id=False):
    return list(map(lambda employee: employee_to_json(employee, with_id=with_id), employees))
