from website.utilitaries import db_connector

conn = db_connector()
cur = conn.cursor()


def get_user_info(user_id):
    query = '''
    select
        *
    from
        medelse.user
    WHERE
        user_id = {user_id};
    '''
    cur.execute(query, (user_id))
    mission_id = cur.fetchone()[0]
    conn.commit()
    return mission_id
