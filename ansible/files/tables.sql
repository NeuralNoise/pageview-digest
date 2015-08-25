CREATE TABLE IF NOT EXISTS theonion_pageviews (
  path    VARCHAR (512) NOT NULL,
  date    TIMESTAMP NOT NULL,
  count   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS avclub_pageviews (
  path    VARCHAR (512) NOT NULL,
  date    TIMESTAMP NOT NULL,
  count   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS clickhole_pageviews (
  path    VARCHAR (512) NOT NULL,
  date    TIMESTAMP NOT NULL,
  count   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS onionstudios_pageviews (
  path    VARCHAR (512) NOT NULL,
  date    TIMESTAMP NOT NULL,
  count   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS starwipe_pageviews (
  path    VARCHAR (512) NOT NULL,
  date    TIMESTAMP NOT NULL,
  count   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS theonion_trends (
  content_id  INTEGER NOT NULL,
  date    TIMESTAMP NOT NULL,
  count   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS avclub_trends (
  content_id  INTEGER NOT NULL,
  date        TIMESTAMP NOT NULL,
  count       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS clickhole_trends (
  content_id  INTEGER NOT NULL,
  date        TIMESTAMP NOT NULL,
  count       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS onionstudios_trends (
  content_id  INTEGER NOT NULL,
  date        TIMESTAMP NOT NULL,
  count       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS starwipe_trends (
  content_id  INTEGER NOT NULL,
  date        TIMESTAMP NOT NULL,
  count       INTEGER NOT NULL
);
