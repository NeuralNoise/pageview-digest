import requests

import psycopg2
import pytest
import testing.postgresql
from pytest_localserver.http import WSGIServer

from pageview_digest.wsgi import application, db_user, db_passwd, db_dbname


@pytest.mark.usefixtures("setup_postgresql")
class TestWSGIApplication:
    @pytest.fixture()
    def setup_postgresql(self):
        self.postgresql = testing.postgresql.Postgresql(port=5432)
        conn = psycopg2.connect(**self.postgresql.dsn())
        conn.autocommit = True
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Create configured user if doesn't exist
        cursor.execute("SELECT COUNT(*) FROM pg_roles WHERE rolname='{}'".format(db_user))
        if cursor.fetchone()[0] <= 0:
            cursor.execute("CREATE USER {0} WITH PASSWORD '{1}'".format(
                db_user, db_passwd
            ))

        # Create configured database
        cursor.execute(
            "SELECT COUNT(*) FROM pg_database WHERE datname='{}'".format(db_dbname)
        )
        if cursor.fetchone()[0] <= 0:
            cursor.execute("CREATE DATABASE {}".format(db_dbname))

        conn.close()
        cursor.close()
        # Connect to the newly created database
        ingest_dsn = self.postgresql.dsn().copy()
        ingest_dsn.update({
            'database': db_dbname,
            'user': db_user,
            'password': db_passwd
        })

        conn = psycopg2.connect(**ingest_dsn)
        conn.autocommit = True
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Load all of our beautiful site tables
        cursor.execute(open('./ansible/files/tables.sql', 'r').read())
        cursor.close()

    @pytest.fixture(autouse=True)
    def testserver(self, request):
        """Defines the testserver funcarg"""
        server = WSGIServer(application=application)
        server.start()
        request.addfinalizer(server.stop)
        server.trending_url = server.url + "/trending.json"
        return server

    def test_response_success(self, testserver):
        """assert app returns a 200"""
        resp = requests.get(testserver.trending_url, params={'site': 'theonion'})
        assert resp.status_code == 200

    def test_offset_parameter_success(self, testserver):
        """assert app returns a 200 when provided an offset parameter"""
        resp = requests.get(testserver.trending_url, params={'site': 'theonion', 'offset': '50'})
        assert resp.status_code == 200

    def test_response_not_found(self, testserver):
        """assert any request not at /trending.json returns 400"""
        resp = requests.get(testserver.url)
        assert resp.status_code == 404
