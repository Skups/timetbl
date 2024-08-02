import psycopg

import click
from flask import Flask, current_app, g
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config


def connect_database(config):
    try:
        with psycopg.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg.DatabaseError, Exception) as error:
        print(error)


def get_database():
    if "db" not in g:
        # conn = connect_database(load_config())
        conn = psycopg.connect(" host=localhost dbname=timetable_db user=postgres password=12345678 ")
        if conn is not None:
            g.database = conn
        else:
            exit()

    return g.database


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_database()

    with current_app.open_resource("schema.sql") as f:
        with db.cursor() as cur:
            cur.execute(f.read().decode("utf8"))
            db.commit()


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)