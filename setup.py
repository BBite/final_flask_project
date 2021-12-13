from setuptools import setup, find_packages

setup(
    name='Department App',
    version='1.0',
    description='Web application to manage departments and employees using web service',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==2.0.2',
        'SQLAlchemy==1.4.27',
        'marshmallow==3.14.1',
        'marshmallow-sqlalchemy==0.26.1',
        'psycopg2==2.9.2',
        'Flask-SQLAlchemy==2.5.1',
        'flask-marshmallow==0.14.0',
        'Flask-Migrate==3.1.0',
        'Flask-RESTful==0.3.9',
        'Flask-WTF==1.0.0',
    ]
)
