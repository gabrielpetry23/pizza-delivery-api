from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from database.schemas import OrderModel
from database.models import Order, User
from database.db import Session, engine
from fastapi.encoders import jsonable_encoder


order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

session = Session(bind=engine)


@order_router.get("/get_orders")
async def get_order(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    if user.is_staff:
        orders = session.query(Order).all()
        if not orders:
            return []
        return jsonable_encoder(orders)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Only staff can view this page!",
    )


@order_router.post("/create_order", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(quantity=order.quantity, pizza_size=order.pizza_size, user=user)

    session.add(new_order)
    session.commit()
    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "order_status": new_order.order_status,
        "id": new_order.id,
    }
    return jsonable_encoder(response)
