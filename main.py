from fastapi import FastAPI
from routes.auth import auth_router
from routes.orders import order_router
from fastapi_jwt_auth import AuthJWT
from database.schemas import Settings

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)


@AuthJWT.load_config
def get_config():
    return Settings()
