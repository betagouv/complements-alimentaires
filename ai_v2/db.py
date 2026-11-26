"""READ-ONLY access to the production database.

The session is opened with `default_transaction_read_only=on`: the server itself refuses any
write, even one made by mistake. No other part of the package opens a database connection.

Connection settings come from the `db_server` ("host:port"), `db_user`, `db_password` and
`db_name` environment variables (`db_name` can also live in the local env file, see config.py).
"""

from __future__ import annotations

import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from .config import Settings

# One connection per worker thread (psycopg connections must not be shared between threads).
_local = threading.local()


def connect(settings: Settings) -> psycopg.Connection:
    if not (settings.db_server and settings.db_user and settings.db_name):
        raise RuntimeError("Database settings missing: set db_server (host:port), db_user, db_password and db_name.")
    host, port = settings.db_server.split(":")
    conn = psycopg.connect(
        host=host,
        port=int(port),
        user=settings.db_user,
        password=settings.db_password,
        dbname=settings.db_name,
        options="-c default_transaction_read_only=on -c statement_timeout=180000",
        connect_timeout=20,
        # A connection dropped server-side must not hang the client forever.
        keepalives=1,
        keepalives_idle=20,
        keepalives_interval=5,
        keepalives_count=3,
        tcp_user_timeout=120000,
        row_factory=dict_row,
    )
    conn.read_only = True
    conn.autocommit = True  # each SELECT is its own read-only transaction
    return conn


@contextmanager
def cursor(settings: Settings):
    conn = getattr(_local, "conn", None)
    if conn is None or conn.closed:
        conn = connect(settings)
        _local.conn = conn
    with conn.cursor() as cur:
        yield cur


def fetchall(settings: Settings, sql: str, params=None, _retry: int = 2) -> list[dict]:
    """Run a SELECT and return the rows as dicts. Reconnects and retries if the server dropped the connection."""
    try:
        with cursor(settings) as cur:
            cur.execute(sql, params or ())
            return list(cur.fetchall())
    except psycopg.OperationalError:
        # Connection closed by the server: open a new (read-only) one and retry.
        conn = getattr(_local, "conn", None)
        if conn is not None:
            try:
                conn.close()
            except Exception:  # noqa: BLE001
                pass
        _local.conn = None
        if _retry <= 0:
            raise
        return fetchall(settings, sql, params, _retry - 1)


def fetchone(settings: Settings, sql: str, params=None) -> dict | None:
    rows = fetchall(settings, sql, params)
    return rows[0] if rows else None


# Few simultaneous connections (the production database has a connection limit): dedicated pool.
DB_EXECUTOR = ThreadPoolExecutor(max_workers=3, thread_name_prefix="db")


async def run_db(fn, *args):
    """Run a blocking DB function in the dedicated thread pool, from async code."""
    return await asyncio.get_running_loop().run_in_executor(DB_EXECUTOR, fn, *args)
