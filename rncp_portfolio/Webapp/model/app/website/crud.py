from website.utilitaries import db_connector

conn = db_connector()
cur = conn.cursor()


def create_mission(office_id, service_name, specialty_name, created_at, tags, hours, pay):
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


def view_mission(mission_id):
    query = '''
    SELECT * from medelse.announcement where id = %s;
    '''
    cur.execute(query, (mission_id,))
    mission_view = cur.fetchone()
    if not mission_view:
        print('No mission to display, could not find matching id')
        return {'No mission to display, could not find matching id'}
    return mission_view


def delete_mission(mission_id):
    query = '''
    DELETE FROM medelse.announcement where id = %s
    RETURNING id;
    '''
    cur.execute(query, (mission_id,))
    mission_id = cur.fetchone()
    if mission_id is None:
        return ('Deletion failed, mission not found')
    conn.commit()
    return mission_id


# print(delete_mission(2))
# # print(create_mission(1, 11, "2025-09-24 11:33:24",
# #       "Announcement.Rhythm.Day", 8, 120, "Nurse"))
# # new_id = create_mission(1, 11, "2025-09-24 11:33:24", "Announcement.Rhythm.Day", 8, 120, "Nurse")
