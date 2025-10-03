from calculators import mission_trios_selector
from website.crud import create_mission, view_mission, delete_mission
from fastapi import FastAPI
from refresher import refresher
from exceptions import IdError, RefreshingError
from fs.errors import ResourceNotFound
from website.pw import add_user
from website.login import login
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # ou ["http://localhost:3000"] si tu veux limiter à ton front
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ********************************************************************************
# WEBSITE


class LoginRequest(BaseModel):
    email: str
    password: str


@app.get("/ping")
def ping():
    try:
        print('pong?')
        return 'pong'
    except Exception as a:
        return a


@app.get("/auth/register/{name}, {first_name}, {passwd}, {email}")
def register(name, first_name, passwd, email):
    try:
        print('register')
        return add_user(name, first_name, passwd, email)
    except Exception as a:
        return a


@app.post("/auth/login")
def logger(body: LoginRequest):
    print('login')

    return login(body.email, body.password)
# def logger(email, password):
#     try:
#         return login(email, password)
#     except Exception as a:
#         return a


@app.post("/missions/")
def create(office_id, service_id, created_at, tags, hours, pay, role):
    print()
    # insert into DB
    return create_mission(office_id, service_id, created_at, tags, hours, pay, role)


@app.get("/missions/{mission_id}")
def view(mission_id: int):
    # fetch from DB to view
    return view_mission(mission_id)


@app.post("/missions/{mission_id}")
def delete(mission_id: int):
    # delete from DB
    return delete_mission(mission_id)

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
    # outputs 30 best trios from users suggestions
    if not user_id.isdigit():
        return {"Please input a valid numeric user_id"}
    try:
        selected_trio, full_trios = mission_trios_selector(
            int(user_id), 30, 0, dominant_category_check=False)
        return full_trios
    except ResourceNotFound:
        return {"Training datas not found, please run the refresher first"}
    except IdError as e:
        return {str(e)}
    except IndexError:
        return {"ID not found for user_id(1):": str(user_id)}
    except TypeError:
        return {"ID not found for user_id:(2)": str(user_id)}
    except Exception as e:
        return {f"An error occured:: {str(e)}, {type(e)}"}


@app.get("/{user_id}/{list_limit}")
def run_with_id_list_limit(user_id: str, list_limit: str):
    # outputs a list of trios from users suggestions up to the 'list_limit' limit
    if not user_id.isdigit():
        return {"Please input a valid numeric user_id"}
    try:
        selected_trio, full_trios = mission_trios_selector(
            int(user_id), int(list_limit), 0, dominant_category_check=False)
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
        return selected_trio
    except IdError:
        return {"ID not found for user_id(0):": str(user_id)}
    except IndexError:
        return {"ID not found for user_id(1):": str(user_id)}
    except TypeError:
        return {"ID not found for user_id(2):": str(user_id), 'with error:': str(e)}
    except Exception as e:
        return {f"An error occured:: {str(e)}, {type(e)}"}


@app.get("/")
def run():
    if __name__ == "__main__":
        return ('Usage: /user_id : Returns 50 best trios for given user_id OR /user_id/list_limit : Returns list_limit best trios for given user_id OR user_id/list_limit/trio_index : Returns trio_index best trio for given user_id')


# print(register('doudou', 'tritri',
#                'coucoubebou', "pipou@pipou.lol"))


# print(register('couilles', 'are',
#                'petitcoeurleplusbeaulove', "coucoulesbebous@tropchoupi.de"))
print(login("coucoulesbebous@tropchoupi.de", "petitcoeurleplusbeaulove"))
