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


@order_router.get("/orders")
async def list_all_orders(Authorize: AuthJWT = Depends()):
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


@order_router.get("/order/{id}")
async def get_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!"
            )
        return jsonable_encoder(order)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Only staff can view this page!",
    )


@order_router.get("/user/orders")
async def get_user_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    return jsonable_encoder(current_user.orders)


@order_router.get("/user/order/{order_id}", response_model=OrderModel)
async def get_user_specific_order(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    subject = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == subject).first()
    orders = current_user.orders

    for order in orders:
        if order.id == id:
            return jsonable_encoder(order)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!"
    )
    
    
@order_router.put("/order/update/{order_id}")
async def update_order(order_id: int, order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
        
        order_to_update = session.query(Order).filter(Order.id == order_id).first()
        order_to_update.quantity = order.quantity
        order_to_update.pizza_size = order.pizza_size
        
        session.commit()
        return jsonable_encoder(order_to_update)
    
