from fastapi import FastAPI
from routes.auth import auth_router
from routes.orders import order_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)

