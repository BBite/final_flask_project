# Department App

## With this app you can:

- ### Display a list of departments and the average salary (calculated automatically) for these departments

- ### Display a list of employees in the departments with an indication of the salary for each employee and a search field to search for employees born on a certain date or in the period between dates

- ### Change (add / edit / delete) the above data

## How to build this project:

- ### Navigate to the project root folder

- ### Install the requirements:

```
pip install -r requirements.txt
```

- ### Set the following environment variables:

```
APP_SETTINGS=config.ProductionConfig
SECRET_KEY=<your_secret_key>
```

- #### Configure PostgreSQL database

```
DATABASE_URL=postgres://<your_username>:<your_password>@<your_database_url>/<your_database_name>
```

- ### Run migrations to create database infrastructure:

```
python -m flask db upgrade
```

- ### (Optional) Populate the database with sample data

```
python populate_db.py
```

- ### Run the project locally:

```
python -m flask run
```

## Now you should be able to access the web service and web application on the following addresses:

- ### Web Service:

```
localhost:5000/api/departments
localhost:5000/api/department/<department_id>

localhost:5000/api/employees
localhost:5000/api/employee/<employee_id>
localhost:5000/api/employees/search
```

- ### Web Application:

```
localhost:5000/

localhost:5000/departments
localhost:5000/departments/new
localhost:5000/departments/<department_id>/edit
localhost:5000/departments/<department_id>/delete

localhost:5000/departments/<department_id>/employees/new
localhost:5000/departments/<department_id>/employees/<employee_id>/edit
localhost:5000/departments/<department_id>/employees/<employee_id>/delete

localhost:5000/employees
localhost:5000/employees/new
localhost:5000/employees/<employee_id>/edit
localhost:5000/employees/<employee_id>/delete