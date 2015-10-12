#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools.command.test import test as TestCommand # noqa

from setuptools import setup

dev_requires = [
    "flake8>=2.0,<2.1",
    "pytest==2.6.4",
    "pytest-dbfixtures==0.12.0",
    "pytest-cov==1.8.1",
    "pytest-localserver==0.3.4",
    "testing.postgresql==1.2.1",
    "coveralls==0.5",
    "mkdocs==0.12.2",
    "requests==2.8.0"
]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name="pageview_digest",
    version="0.0.5",

    packages=["pageview_digest", ],
    install_requires=["gevent==1.0.2", "psycopg2==2.6.1", "pylibmc==1.5.0", "python-dateutil==2.4.2", ],

    author="Vince Forgione",
    author_email="vforgione@theonion.com",
    description="A simple, fast uwsgi/gevent application to dump pageview data from Postgres",
    license="MIT",
    keywords=["uwsgi gevent postgres pageview"],
    url="https://github.com/theonion/pageview-digest",
    tests_require=dev_requires,
    extras_require={
        'dev': dev_requires,
    },
    cmdclass={'test': PyTest}
)
