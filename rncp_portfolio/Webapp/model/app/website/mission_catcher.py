from website.utilitaries import db_connector

conn = db_connector()
cur = conn.cursor()


def fetch_mission(office_id, service_name, specialty_name, created_at, tags, hours, pay):
    query = '''
    INSERT INTO MEDELSE.ANNOUNCEMENT 
        (office_id, service_name, specialty_name, created_at, tags, hours, pay) 
    VALUES
        (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    '''
    cur.execute(query, (office_id, service_name, specialty_name,
                created_at, tags, hours, pay))
    mission_id = cur.fetchone()[0]
    conn.commit()
    return mission_id
