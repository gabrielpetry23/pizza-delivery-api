from fastapi import FastAPI
from routes.auth import auth_router
from routes.orders import order_router
from fastapi_jwt_auth import AuthJWT
from database.schemas import Settings
from fastapi.openapi.utils import get_openapi

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)


@AuthJWT.load_config
def get_config():
    return Settings()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Pizza Delivery API",
        version="1.0.0",
        description="API para gerenciamento do sistema de entrega de pizzas",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi