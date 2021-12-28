from setuptools import find_packages, setup

setup(
    name='smart_room_backend',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'python-dotenv',
        'Flask-SQLAlchemy',
        'Flask-JWT-Extended',
        'validators',
        'mysqlclient',
    ],
)