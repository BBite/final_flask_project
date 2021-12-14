"""
Department views used to manage departments on web application,
this module defines the following functions:

- `get_departments`: function that displays all departments page
- `get_department`: function that displays department page
- `add_department`: function that manages creation of new department
- `edit_department`: function that manages update of department
- `delete_department`: function that deletes department
"""

from flask import Blueprint, render_template, redirect, url_for, flash, abort

from department_app import app

from department_app.schemas.department_schema import DepartmentSchema
from department_app.service.department_service import DepartmentService
from department_app.forms.department_form import DepartmentForm

from department_app.views.employee_view import nested_employees_blueprint

departments_blueprint = Blueprint('departments', __name__, url_prefix='/departments')

departments_blueprint.register_blueprint(nested_employees_blueprint)

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)


@app.route('/')
@departments_blueprint.route('/')
def get_departments():
    """
    Fetches all departments via service
    Renders 'departments.html' template

    :return: rendered 'departments.html' template
    """
    departments = DepartmentService.get_departments()
    departments = departments_schema.dump(departments)

    app.logger.debug(f'Data: {departments}')
    app.logger.debug('departments.html was rendered')

    return render_template('departments.html', departments=departments), 200


@departments_blueprint.route('/<int:department_id>')
def get_department(department_id):
    """
    Fetches the department with given id via service
    Renders 'department.html' template

    :param int department_id: id of the department
    :return: rendered 'department.html' template
    """
    department = DepartmentService.get_department_by_id(department_id)
    if not department:
        app.logger.error(f'There is no department with given id({department_id})')
        abort(404)
    department = department_schema.dump(department)

    app.logger.debug(f'Data: {department}')
    app.logger.debug('department.html was rendered')

    return render_template('department.html', department=department), 200


@departments_blueprint.route('/new', methods=['GET', 'POST'])
def add_department():
    """
    Deserializes request data
    Uses service to add the department to the database
    Renders 'department_form.html' template or
    redirect to 'get_departments' page in case of successful input
    Displays validation errors

    :return: rendered 'department_form.html' template or
    redirect to 'get_departments' page in case of successful input
    """
    form = DepartmentForm()

    if form.validate_on_submit():
        department_json = {'name': form.name.data}
        app.logger.debug(f'Data: {department_json}')
        DepartmentService.add_department(department_json)
        flash('Department has been created successfully', category='success')
        return redirect(url_for('.get_departments'))

    for field_name, error_messages in form.errors.items():
        for err in error_messages:
            flash(f'{form[field_name].name.replace("_", " ").capitalize()}: {err}',
                  category='danger')
            app.logger.error(f'{form[field_name].label.text}{err}')

    app.logger.debug('department_form.html was rendered')

    return render_template('department_form.html',
                           department={}, form=form, new=True, prev_input=form.data), 200


@departments_blueprint.route('/<int:department_id>/edit', methods=['GET', 'POST'])
def edit_department(department_id):
    """
    Deserializes request data
    Uses service to update the department with given id
    Renders 'department_form.html' template or
    redirect to 'get_department' page that was updated in case of successful input
    Displays validation errors

    :param int department_id: id of the department to be updated
    :return: rendered 'department_form.html' template or
    redirect to 'get_department' page that was updated in case of successful input
    """

    form = DepartmentForm()

    department = DepartmentService.get_department_by_id(department_id)
    if not department:
        app.logger.error(f'There is no department with given id({department_id})')
        abort(404)

    if form.validate_on_submit():
        department_json = {'name': form.name.data}
        app.logger.debug(f'Data: {department_json}')
        DepartmentService.update_department(department_id, department_json)
        flash('Department has been updated successfully', category='success')
        return redirect(url_for('.get_department', department_id=department_id))

    # allows to submit when nothing changes
    if (len(form.errors) == 1 and len(form.errors['name']) == 1
            and form.errors['name'][0] == 'Department with such name already exists'
            and department == DepartmentService.get_department_by_name(form.name.data)):
        flash('Department has been updated successfully', category='success')
        return redirect(url_for('.get_department', department_id=department_id))

    for field_name, error_messages in form.errors.items():
        for err in error_messages:
            flash(f'{form[field_name].name.replace("_", " ").capitalize()}: {err}',
                  category='danger')
            app.logger.error(f'{form[field_name].label.text}{err}')

    department = department_schema.dump(department)

    app.logger.debug(f'Data: {department}')
    app.logger.debug('department_form.html was rendered')

    return render_template('department_form.html', department=department, form=form, new=False,
                           prev_input=form.data), 200


@departments_blueprint.route('/<int:department_id>/delete')
def delete_department(department_id):
    """
    Uses service to delete the department with given id
    Returns redirect to 'get_departments' page

    :param int department_id: id of the department to be deleted
    :return: redirect to 'get_departments' page
    """
    department = DepartmentService.get_department_by_id(department_id)
    if not department:
        app.logger.error(f'There is no department with given id({department_id})')
        abort(404)
    DepartmentService.delete_department(department_id)
    flash('Department has been deleted successfully', category='success')
    return redirect(url_for('.get_departments'))
