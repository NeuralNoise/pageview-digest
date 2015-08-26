#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import logging
import json
import os

from dateutil import tz
import pylibmc
import psycopg2
import psycopg2.extras

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs


logger = logging.getLogger('digest')
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

db_host = os.environ.get("DIGEST_DB_HOST", "localhost")
db_port = os.environ.get("DIGEST_DB_PORT", "5432")
db_user = os.environ.get("DIGEST_DB_USER", "ingest")
db_passwd = os.environ.get("DIGEST_DB_PASSWD", "ingest")
db_dbname = os.environ.get("DIGEST_DB_DBNAME", "ingest")

utc = tz.gettz('UTC')
central = tz.gettz('America/Chicago')

memcached_hosts = os.environ.get("DIGEST_MEMCACHED_HOSTS", "localhost").split(",")
memcached_client = pylibmc.Client(memcached_hosts)
cache_duration = 30 * 60  # seconds

DEFAULT_OFFSET = 30  # minutes
DEFAULT_LIMIT = 50


def get_trending_data(site, offset=DEFAULT_OFFSET, limit=DEFAULT_LIMIT):
    cache_key = "pageview_digest_{}_{}_{}".format(site, offset, limit)
    try:
        cached = memcached_client.get(cache_key)
        if cached:
            return cached
    except Exception as e:
        logger.exception(e)

    connection = psycopg2.connect(database=db_dbname, user=db_user, password=db_passwd, host=db_host, port=db_port)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    naive_now = datetime.now()
    offsetted = naive_now - timedelta(minutes=offset)
    offsetted = offsetted.replace(tzinfo=utc)
    date = offsetted.astimezone(central)

    query = "SELECT content_id, SUM(count) as count " \
            "FROM {}_trends " \
            "WHERE date >= '{}' " \
            "GROUP BY content_id " \
            "ORDER BY SUM(count) DESC " \
            "LIMIT {};".format(site, date, limit)
    cursor.execute(query)
    records = cursor.fetchall()

    trending = [{
        "content_id": r["content_id"],
        "score": r["count"]
    } for r in records]
    payload = json.dumps(trending)

    try:
        memcached_client.set(cache_key, payload, time=cache_duration)
    except Exception as e:
        logger.exception(e)

    return payload


def application(env, start_response):
    path = env["PATH_INFO"]
    params = parse_qs(env["QUERY_STRING"])

    if path == "/trending.json" and "site" in params:
        try:
            site = params.get("site", [None])[0]
            offset = params.get("offset", [DEFAULT_OFFSET])[0]
            limit = params.get("limit", [DEFAULT_LIMIT])[0]
            payload = get_trending_data(site, offset, limit)
            start_response("200 OK", [("Content-Type", "application/json")])
            yield payload
        except Exception as e:
            logger.exception(e)
            start_response("400 Bad Request", [("Content-Type", "text/plain")])
            yield "Your request erred. Check the logs to find out what happened."

    else:
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        yield ""
