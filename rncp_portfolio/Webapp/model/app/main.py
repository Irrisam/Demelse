from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from website.crud import create_mission, view_mission, delete_mission
from website.pw import add_user
from website.login import login
from refresher import refresher

app = FastAPI()

# ✅ Autoriser ton front (Nuxt)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # A restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# MODELS
# --------------------------


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    first_name: str
    email: str
    password: str


class MissionCreationRequest(BaseModel):
    office_id: int
    service_id: int
    created_at: str
    tags: str
    hours: float
    pay: float
    role: str


class MissionViewRequest(BaseModel):
    id: int
# --------------------------
# ROUTES
# --------------------------


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.post("/auth/register")
def register(body: RegisterRequest):
    try:
        user = add_user(body.name, body.first_name, body.password, body.email)
        return {"success": True, "user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login")
def logger(body: LoginRequest):
    try:
        token = login(body.email, body.password)
        return {"success": True, "access_token": token}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/missions/create")
def create_mission_route(body: MissionCreationRequest):
    try:
        id = create_mission(body.office_id, body.service_id,
                            body.created_at, body.tags, body.hours, body.pay, body.role)
        return {"success": True, "id": id}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid mission infos")


@app.get("/missions/view/{mission_id}")
def view_mission_route(body: MissionViewRequest):
    id = view_mission(body.id)
    return id


@app.delete("/missions/delete/{mission_id}")
def delete_mission_route(mission_id: int):
    return delete_mission(mission_id)


@app.get("/refresher")
def refresh():
    try:
        refresher()
        return {"success": True, "message": "Training data refreshed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 'tristan', 'duchamp', 'Clementine17', 'tristanduchamp@hotmail.fr'))
