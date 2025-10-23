import bcrypt
import jwt
import datetime
from website.utilitaries import db_connector
import os

JWT_TOKEN = os.getenv("JWT_SECRET", "fallback-secret")

conn = db_connector()
cur = conn.cursor()


def verify_password(password, hashed_pw):
    if isinstance(hashed_pw, str):
        hashed_pw = hashed_pw.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pw)


def create_jwt_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, JWT_TOKEN, algorithm="HS256")
    return token


def login(email, password):
    cur.execute(
        'SELECT id, hashed_password from medelse.user where email = %s', (email,))
    result = cur.fetchone()
    if not result:
        return {"error": "Invalid email or password(1)"}
    user_id, hashed_pw = result
    if not verify_password(password, hashed_pw):
        return {"error": "Invalid email or password(2)"}
    token = create_jwt_token(user_id)
    return {"access_token": token}


def get_user_id_from_token(token):
    try:
        decoded = jwt.decode(token, JWT_TOKEN, algorithms=["HS256"])
        return decoded.get("user_id")
    except jwt.ExpiredSignatureError:
        return {"error": "Token expiré"}
    except jwt.InvalidTokenError:
        return {"error": "Token invalide"}
# print(login('pipou@pipou.lol', 'coucoubebou'))
