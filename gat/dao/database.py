import psycopg2

from gat.util import config


def execute(command, dql):
    connection = connect()
    cur = connection.cursor()
    try:
        cur.execute(command)
    except:
        connection = connect()
        cur = connection.cursor()
        cur.execute(command)
    ret = None
    if dql:
        ret = cur.fetchall()
    else:
        connection.commit()
    cur.close()
    connection.close()
    return ret


def connect():
    connection = None
    try:
        # TODO might have a problem here
        params = config.config("static/resources/security/database_config.ini", "postgresql")
        connection = psycopg2.connect(**params)
    except:
        raise Exception("Error connecting to database.")
    return connection
