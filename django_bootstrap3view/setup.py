#!/usr/bin/env python
import os
from setuptools import setup, find_packages

#define variables for setup.py
__author__ = 'Ernesto Bossi'
__version__ = "0.0.7"

__dir__ = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(__dir__, "django_bootstrap3view_app", "management", "commands", "templates")
templates_files = [os.path.join(templates_dir, file) for file in os.listdir(templates_dir)]

setup(
    name='django-classview-bootstrap3',
    version=__version__,
    description='Django-Bootstrap 3 generic template with class views',
    author=__author__,
    license="BSD-3",
    author_email='bossi.ernestog@gmail.com',
    url='http://bossiernesto.github.io/django-bootstrap3-classview/',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2.7",
    ],
    packages=find_packages(exclude=["django_bootstrap3view"]),
    data_files=[
        (templates_dir, templates_files), ('',["LICENSE.txt","changelog.md"])
    ],
    include_package_data=True,
    install_requires=[
        "django_conventions",
        "south",
        "django-webtest",
        "dj_database_url",
        "simplejson",
        "csv",
    ],
    scripts=['bin/create_bootstrap_project'],
)

