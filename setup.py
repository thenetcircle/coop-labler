#!/usr/bin/env python

from setuptools import setup, find_packages


version = '0.1.0-dev'

setup(
    name='labler',
    version=version,
    description="Co-Operative Labler",
    long_description="""Co-Operative labling of training data.""",
    classifiers=[],
    author='Service Team @ TNC',
    author_email='contact@thenetcircle.com',
    url='https://github.com/thenetcircle/coop-labler',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'labler = labler.cli:entrypoint',
        ],
    },
    install_requires=[
        'codecov',
        'coverage',
        'Flask',
        'Flask-RESTful',
        'flask-sqlalchemy',
        'Flask-Testing',
        'gitpython',
        'gnenv',
        'greenlet',
        'gunicorn',
        'nose',
        'nose-parameterized',
        'numpy',
        'python-dateutil',
        'PyYAML',
        'scipy',
        'sqlalchemy',
        'statsd',
        'typing',
        'yapsy',
    ])
