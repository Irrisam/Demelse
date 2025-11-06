from calculators import mission_trios_selector, cast_to_int
from website.crud import create_mission, view_mission, delete_mission
from website.login import get_user_id_from_token
from fastapi import FastAPI, HTTPException, requests, Response, Request
from website.web_db_tools import get_user_info, update_user_info, get_pros_list, get_mission_list, get_missions, missions_by_categories

from refresher import refresher
from website.utilitaries import normalize_model_output
from exceptions import IdError, RefreshingError
from fs.errors import ResourceNotFound
from website.pw import add_user
from website.login import login
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import json

# uvicorn main:app --reload --port 8000

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: str
    password: str


class UserUpdateRequest(BaseModel):
    user_id: int
    name: str
    first_name: str
    email: str


class RegisterRequest(BaseModel):
    name: str
    first_name: str
    email: str
    password: str


class MissionCreationRequest(BaseModel):
    office_id: int
    service_name: str
    specialty_name: str
    created_at: str
    tags: str
    hours: float
    pay: float


class UserInfoRequest(BaseModel):
    userId: int


class MissionViewRequest(BaseModel):
    id: int


class ProIDRequest(BaseModel):
    professional_id: int


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
        id = create_mission(body.office_id, body.service_name, body.specialty_name,
                            body.created_at, body.tags, body.hours, body.pay)
        return {"success": True, "id": id}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid mission infos")


@app.get("/missions/view/{mission_id}")
def view_mission_route(mission_id: int):
    mission = view_mission(mission_id)
    if isinstance(mission, dict) and "error" in mission:
        return mission
    return {
        "id": mission[0],
        "office_id": mission[1],
        "created_at": mission[2],
        "tags": mission[3],
        "hours": mission[4],
        "pay": mission[5],
        "service_name": mission[6],
        "specialty_name": mission[7]
    }


@app.delete("/missions/delete/{mission_id}")
def delete_mission_route(mission_id: int):
    return delete_mission(mission_id)


@app.post("/account/id_fetch")
async def fetch_id_route(request: Request):
    body = await request.json()
    token = body.get("token")
    return get_user_id_from_token(token)


@app.post("/account/user_info")
def get_user_infos_route(body: UserInfoRequest):
    return get_user_info(body.userId)


@app.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key="token")
    return {"message": "Déconnecté"}


@app.put("/auth/info_update")
def update_user_info_route(body: UserUpdateRequest):
    try:
        update_user_info(body.user_id, body.name, body.first_name, body.email)
        return {"success": True, "message": "User info updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/datas/list/missions")
def list_missions(body: UserInfoRequest):
    return get_mission_list(body.userId)


@app.post("/algos/best_categories")
def best_categories(body: ProIDRequest):
    raw = run_with_id_list_limit(str(body.professional_id), "3")

    if isinstance(raw, dict):
        return {
            "error": True,
            "message": list(raw.keys())[0],
            "detail": list(raw.values())[0]
        }

    return normalize_model_output(raw)


@app.post("/datas/list/pros")
def list_pros(body: UserInfoRequest):
    status = get_pros_list(body.userId)

    if status is None:
        raise HTTPException(status_code=404, detail="No professionals found")
    return status


@app.get("/all_pro_missions_fetch")
def pro_missions_fetch():
    missions = get_missions()
    if missions is None:
        raise HTTPException(status_code=404, detail="No missions found")
    return missions


@app.post("/algos/missions_by_categories")
def missions_by_categories_route(body: dict):
    missions = missions_by_categories(body)
    if missions is None:
        raise HTTPException(
            status_code=404, detail="No missions found for the given categories")
    return missions
# ********************************************************************************
# MICROSERVICE AI


@app.get("/refresher")
def refresh():
    try:
        refresher()
        return {"Training datas refreshed"}
    except RefreshingError as e:
        return {e}
    except Exception as e:
        return {f"Training datas refreshing failed:: {type(e)} - {str(e)}"}


@app.get("/{user_id}")
def run_with_id(user_id: str):
    print(
        '\nRoute used for demonstration: @app.get("/{user_id}"), run_with_id(), default route returning 30 trios\n')
    # outputs 30 best trios from users suggestions
    if not user_id.isdigit():
        return {"error": "Please input a valid numeric user_id"}

    try:
        print('Generating trios for user_id:', user_id)
        print('\n')
        _, full_trios = mission_trios_selector(
            int(user_id), 30, 0, dominant_category_check=False
        )
        full_trios = cast_to_int(full_trios)

        with open("results.json", "w", encoding="utf-8") as f:
            json.dump(full_trios, f, ensure_ascii=False, indent=4)

        return full_trios

    except ResourceNotFound:
        error_msg = {
            "error": "Training datas not found, please run the refresher first"}
    except IdError as e:
        error_msg = {"error": str(e)}
    except IndexError:
        error_msg = {"error": f"ID not found for user_id(1): {user_id}"}
    except TypeError:
        error_msg = {"error": f"ID not found for user_id(2): {user_id}"}
    except Exception as e:
        error_msg = {"error": f"An error occurred: {str(e)}, {type(e)}"}

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(error_msg, f, ensure_ascii=False, indent=4)

    return error_msg


@app.get("/{user_id}/{list_limit}")
def run_with_id_list_limit(user_id: str, list_limit: str):
    # outputs a list of trios from users suggestions up to the 'list_limit' limit
    if not user_id.isdigit():
        return {"Please input a valid numeric user_id"}
    try:
        selected_trio, full_trios = mission_trios_selector(
            int(user_id), int(list_limit), 0, dominant_category_check=False)
        full_trios = cast_to_int(full_trios)
        return full_trios
    except IdError:
        return {"ID not found for user_id(0):": str(user_id)}
    except IndexError:
        return {"ID not found for user_id(1):": str(user_id)}
    except TypeError:
        return {"ID not found for user_id(2):": str(user_id)}
    except Exception as e:
        return {f"An error occured:: {str(e)}, {type(e)}"}


@app.get("/{user_id}/{list_limit}/{trio_index}")
def run_with_id_list_limit_index(user_id: str, list_limit: str, trio_index: str):
    # outputs a single indexed trio from users suggestions within the 'list_limit' range
    if not user_id.isdigit():
        return {"Please input a valid numeric user_id"}
    try:
        selected_trio, full_trios = mission_trios_selector(int(user_id), int(
            list_limit), int(trio_index), dominant_category_check=False)
        full_trios = cast_to_int(full_trios)
        return selected_trio
    except IdError:
        return {"ID not found for user_id(0):": str(user_id)}
    except IndexError:
        return {"ID not found for user_id(1):": str(user_id)}
    except TypeError:
        return {"ID not found for user_id(2):": str(user_id)}
    except Exception as e:
        return {f"An error occured:: {str(e)}, {type(e)}"}


print(run_with_id("22"))
