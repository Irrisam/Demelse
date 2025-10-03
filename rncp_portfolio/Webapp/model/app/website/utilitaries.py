import psycopg2


def db_connector():

    conn = psycopg2.connect(
        host="localhost",
        dbname="medelse",
        user="tristan",
        password=""
    )

    return (conn)
