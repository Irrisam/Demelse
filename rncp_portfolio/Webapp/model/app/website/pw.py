import bcrypt
from website.utilitaries import db_connector


def pwhasher(pw):
    # convert to bytes
    bytes_pw = pw.encode('utf-8')
    # build salt
    hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
    # building hased pw
    return hashed_pw.decode('utf-8')


# *******************************************************
# REGISTER
conn = db_connector()
cur = conn.cursor()


def user_exists(name, first_name, email):
    query = """
    SELECT 1 FROM medelse.user
    WHERE name = %s AND first_name = %s AND email = %s;
    """

    cur.execute(query, (name, first_name, email))
    return cur.fetchone() is not None


def add_user(name, first_name, password, email):
    if user_exists(name, first_name, email):
        print("User already exists")
        return False

    hashed_pw = pwhasher(password)

    query = """
    INSERT INTO medelse.user (name, first_name, hashed_password, email)
    VALUES (%s, %s, %s, %s);
    """
    cur.execute(query, (name, first_name, hashed_pw, email))
    conn.commit()
    print("User added successfully!")
    return True
