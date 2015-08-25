from setuptools import setup

setup(
    name="pageview_digest",
    version="0.0.1",

    packages=["pageview_digest", ],
    install_requires=["gevent==1.0.2", "psycopg2==2.6.1", "pylibmc==1.5.0", "pytz==2015.4", ],

    author="Vince Forgione",
    author_email="vforgione@theonion.com",
    description="A simple, fast uwsgi/gevent application to dump pageview data from Postgres",
    license="MIT",
    keywords=["uwsgi gevent postgres pageview"],
    url="https://github.com/theonion/pageview-digest",
)
