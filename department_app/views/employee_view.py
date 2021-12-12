"""
Employees views used to manage employees on web application,
this module defines the following functions:

- `pull_department_id`: function that parses department_id value from url
- `get_employees`: function that displays all employees page
- `get_employee`: function that displays employee page
- `add_employee`: function that manages creation of new employee
- `edit_employee`: function that manages update of employee
- `delete_employee`: function that deletes employee
"""

from flask import Blueprint, render_template, redirect, url_for, flash, g, abort

from department_app import app
from department_app.schemas.employee_schema import EmployeeSchema
from department_app.service.employee_service import EmployeeService
from department_app.forms.employee_form import EmployeeForm, FilterForm

from department_app.schemas.department_schema import DepartmentSchema
from department_app.service.department_service import DepartmentService

employees_blueprint = Blueprint('employees', __name__, url_prefix='/employees')
nested_employees_blueprint = Blueprint('employees', __name__,
                                       url_prefix='/<int:department_id>/employees')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
department_schema = DepartmentSchema()


@nested_employees_blueprint.url_value_preprocessor
def pull_department_id(endpoint, values):
    """
    Parse department_id value from url and adds it to request context

    :return: None
    """

    # pylint: disable=assigning-non-slot, unused-argument

    g.department_id = values.pop('department_id')
    if g.department_id:
        app.logger.debug(f'Department id({g.department_id}) was added to request context')


@employees_blueprint.route('/', methods=['GET', 'POST'])
def get_employees():
    """
    Fetches all employees filtered by params via service
    Renders 'employees.html' template

    :return: rendered 'employees.html' template
    """
    form = FilterForm()

    employees = EmployeeService.get_employees()

    if form.validate_on_submit():
        filter_params = {
            'name': form.name.data.strip(),
            'department': form.department.data.strip(),
            'start_salary': (float(form.start_salary.data) if form.start_salary.data
                             else form.start_salary.data),
            'end_salary': (float(form.end_salary.data) if form.end_salary.data
                           else form.end_salary.data),
            'start_date': None,
            'end_date': None,
            'in_date': None
        }
        app.logger.debug(f'Filter params: {filter_params}')
        if form.date_input_type.data == 'in':
            filter_params['in_date'] = form.start_date.data
        elif form.date_input_type.data == 'between':
            filter_params['start_date'] = form.start_date.data
            filter_params['end_date'] = form.end_date.data

        employees = EmployeeService.get_filtered_employees(filter_params)
    else:
        for field_name, error_messages in form.errors.items():
            for err in error_messages:
                flash(f'{form[field_name].label.text}{err}', category='danger')
                app.logger.error(f'{form[field_name].label.text}{err}')

    app.logger.debug(f'Data: {employees}')
    app.logger.debug('employees.html was rendered')

    employees = employees_schema.dump(employees)

    return render_template('employees.html', employees=employees, form=form, prev_input=form.data)


@nested_employees_blueprint.route('/<int:employee_id>')
@employees_blueprint.route('/<int:employee_id>')
def get_employee(employee_id):
    """
    Fetches the employee with given id via service
    Renders 'employee.html' template

    :param int employee_id: id of the employee
    :return: rendered 'employee.html' template
    """
    department_id = g.get('department_id', None)

    if department_id:
        department = DepartmentService.get_department_by_id(department_id)
        if not department:
            app.logger.error(f'There is no department with given id({department_id})')
            abort(404)

    employee = EmployeeService.get_employee_by_id(employee_id)
    if not employee:
        app.logger.error(f'There is no employee with given id({employee_id})')
        abort(404)

    employee = employee_schema.dump(employee)

    app.logger.debug(f'Data: {employee}')
    app.logger.debug('employee.html was rendered')

    return render_template('employee.html', employee=employee, department_id=department_id,
                           from_department=bool(department_id)), 200


@nested_employees_blueprint.route('/new', methods=['GET', 'POST'])
@employees_blueprint.route('/new', methods=['GET', 'POST'])
def add_employee():
    """
    Deserializes request data
    Uses service to add the employee to the database
    Renders 'employee_form.html' template or
    redirect to 'get_employees' page in case of successful input or
    redirect to 'get_department' page in case of department_id is in url
    Displays validation errors

    :return: rendered 'employee_form.html' template or
    redirect to 'get_employees' page in case of successful input or
    redirect to 'get_department' page in case of department_id is in url
    """
    department_id = g.get('department_id', None)

    department = {}

    form = EmployeeForm()
    if department_id:
        department = DepartmentService.get_department_by_id(department_id)
        if not department:
            app.logger.error(f'There is no department with given id({department_id})')
            abort(404)

        department = department_schema.dump(department)

        form.with_department()

    if form.validate_on_submit():
        employee_json = {key: form[key].data for key in form.data
                         if key not in ['submit', 'csrf_token']}
        employee_json['date_of_birth'] = employee_json['date_of_birth'].strftime('%d.%m.%Y')
        employee_json['department'] = {'name': (department['name'] if department_id
                                                else employee_json['department'])}
        app.logger.debug(f'Data: {employee_json}')
        EmployeeService.add_employee(employee_json)
        flash('Employee has been created successfully', category='success')
        return redirect(url_for('departments.get_department',
                                department_id=department_id) if department_id
                        else url_for('employees.get_employees'))

    for field_name, error_messages in form.errors.items():
        for err in error_messages:
            flash(f'{form[field_name].label.text}{err}', category='danger')
            app.logger.error(f'{form[field_name].label.text}{err}')

    app.logger.debug('employee_form.html was rendered')

    return render_template('employee_form.html',
                           employee={}, department=department, form=form, new=True,
                           from_department=bool(department_id), prev_input=form.data), 200


@nested_employees_blueprint.route('/<int:employee_id>/edit', methods=['GET', 'POST'])
@employees_blueprint.route('/<int:employee_id>/edit', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """
    Deserializes request data
    Uses service to update the employee with given id
    Renders 'employee_form.html' template or
    redirect to 'get_employee' page that was updated in case of successful input
    Displays validation errors

    :param int employee_id: id of the employee to be updated
    :return: rendered 'employee_form.html' template or
    redirect to 'get_employee' page that was updated in case of successful input
    """
    department_id = g.get('department_id', None)

    employee = EmployeeService.get_employee_by_id(employee_id)
    if not employee:
        app.logger.error(f'There is no employee with given id({employee_id})')
        abort(404)

    employee = employee_schema.dump(employee)

    department = {}

    form = EmployeeForm()

    if department_id:
        department = DepartmentService.get_department_by_id(department_id)
        if not department:
            app.logger.error(f'There is no department with given id({department_id})')
            abort(404)

        department = department_schema.dump(department)
        form.with_department()

    if form.validate_on_submit():
        employee_json = {key: form[key].data for key in form.data
                         if key not in ['submit', 'csrf_token']}
        employee_json['date_of_birth'] = employee_json['date_of_birth'].strftime('%d.%m.%Y')
        employee_json['department'] = {'name': (department['name'] if department_id
                                                else employee_json['department'])}
        app.logger.debug(f'Data: {employee_json}')
        EmployeeService.update_employee(employee_id, employee_json)

        flash('Employee has been updated successfully', category='success')
        return redirect(url_for(('departments.' if department_id else '')
                                + 'employees.get_employee',
                                department_id=department_id, employee_id=employee_id))

    for field_name, error_messages in form.errors.items():
        for err in error_messages:  # pragma: no cover
            flash(f'{form[field_name].label.text}{err}', category='danger')
            app.logger.error(f'{form[field_name].label.text}{err}')

    app.logger.debug('employee_form.html was rendered')

    return render_template('employee_form.html',
                           employee=employee, department=department, form=form, new=False,
                           from_department=bool(department_id), prev_input=form.data), 200


@nested_employees_blueprint.route('/<int:employee_id>/delete')
@employees_blueprint.route('/<int:employee_id>/delete')
def delete_employee(employee_id):
    """
    Uses service to delete the employee with given id
    Returns redirect to 'get_employees' page or
    redirect to 'edit_department' page in case of department_id is in url

    :param int employee_id: id of the employee to be deleted
    :return: redirect to 'get_employees' page or
    redirect to 'edit_department' page in case of department_id is in url
    """
    department_id = g.get('department_id', None)

    if department_id:
        department = DepartmentService.get_department_by_id(department_id)
        if not department:
            app.logger.error(f'There is no department with given id({department_id})')
            abort(404)

    employee = EmployeeService.get_employee_by_id(employee_id)
    if not employee:
        app.logger.error(f'There is no employee with given id({employee_id})')
        abort(404)

    EmployeeService.delete_employee(employee_id)
    flash('Employee has been deleted successfully', category='success')
    return redirect(url_for('departments.edit_department',
                            department_id=department_id) if department_id
                    else url_for('employees.get_employees'))
