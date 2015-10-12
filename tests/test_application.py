import pytest
from pytest_localserver.http import WSGIServer

import requests

from pageview_digest.wsgi import application


def pytest_funcarg__testserver(request):
    """Defines the testserver funcarg"""
    server = WSGIServer(application=application)
    server.start()
    request.addfinalizer(server.stop)
    server.trending_url = server.url + "/trending.json"
    return server


def test_response_success(testserver):
    """assert app returns a 200"""
    import pdb; pdb.set_trace()
    resp = requests.get(testserver.trending_url, params={'site': 'onion'})
    assert resp.status_code == 200


def test_response_not_found(testserver):
    """assert any request not at /trending.json returns 400"""
    resp = requests.get(testserver.url)
    assert resp.status_code == 404
