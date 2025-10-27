from website.utilitaries import db_connector

conn = db_connector()
cur = conn.cursor()


def get_user_info(user_id):
    query = """
        SELECT id, name, first_name, email
        FROM medelse.user
        WHERE id = %s;
    """
    cur.execute(query, (user_id,))
    user = cur.fetchone()
    if not user:
        return {"error": "Utilisateur introuvable"}
    return {
        "id": user[0],
        "firstname": user[1],
        "lastname": user[2],
        "email": user[3]
    }


def update_user_info(user_id, name, first_name, email):
    query = '''
    UPDATE
        medelse.user
    SET
        name = %s,
        first_name = %s,
        email = %s
    WHERE
        id = %s;
    '''
    cur.execute(query, (name, first_name, email, user_id))
    conn.commit()


def get_pros_list(user_id):

    query = """
        SELECT id, name, first_name, email
        FROM medelse.user
        WHERE is_admin = FALSE AND id != %s;
    """

    cur.execute(query, (user_id,))
    pros = cur.fetchall()
    pros_list = []
    for pro in pros:
        pros_list.append({
            "id": pro[0],
            "firstname": pro[1],
            "lastname": pro[2],
            "email": pro[3]
        })
    return pros_list


def get_mission_list(user_id):
    query = """
        SELECT id, office_id, created_at, tags, hours, pay, service_name, specialty_name
        FROM medelse.announcement;
    """

    cur.execute(query)
    missions = cur.fetchall()

    mission_list = []
    for m in missions:
        mission_list.append({
            "id": m[0],
            "office_id": m[1],
            "created_at": m[2],
            "tags": m[3],
            "hours": m[4],
            "pay": m[5],
            "service_name": m[6],
            "specialty_name": m[7]
        })
    return mission_list
