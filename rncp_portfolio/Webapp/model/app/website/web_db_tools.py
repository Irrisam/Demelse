from website.utilitaries import db_connector
from fastapi import HTTPException

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
        SELECT id, office_id, created_at, tags, hours, pay, service_name, specialty_name, service_id
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
            "specialty_name": m[7],
            "service_id": m[8]
        })

    return mission_list


def get_current_user(user_id: int):
    query = """
        select is_admin from medelse.user where id = %s;
    """
    cur.execute(query, (user_id,))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"is_admin": user[0]}


def get_missions():
    query = """
        SELECT id, office_id, created_at, tags, hours, pay,
               service_name, specialty_name, service_id
        FROM medelse.announcement
        ORDER BY created_at DESC;
    """
    cur.execute(query)
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    missions = [dict(zip(cols, row)) for row in rows]
    return missions


def missions_by_categories(body: dict):
    categories = body.get("categories", [])
    if not categories:
        return []

    ignored_context = {"clinic", "hospi", "hea_cen"}
    categories = [c for c in categories if c.lower() not in ignored_context]

    if not categories:
        return []

    filters = []
    params = []
    for cat in categories:
        cat_lower = cat.lower()
        filters.append("""
            (LOWER(service_name) LIKE %s OR
             LOWER(specialty_name) LIKE %s OR
             LOWER(tags) LIKE %s)
        """)
        params.extend([f"%{cat_lower}%"] * 3)

    query = f"""
        SELECT id, service_name, specialty_name, tags, created_at, hours, pay
        FROM medelse.announcement
        WHERE {" AND ".join(filters)}
          AND created_at > NOW()
        ORDER BY created_at ASC;
    """

    print("🧠 Query exécutée :", query)
    print("🧩 Params :", params)

    cur.execute(query, params)
    results = cur.fetchall()

    columns = [desc[0] for desc in cur.description]
    missions = [dict(zip(columns, row)) for row in results]

    return missions
