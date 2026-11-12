from enum import StrEnum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Noor Foods Orders API")


class OrderStatus(StrEnum):
    PENDING = "pending"
    DELIVERED = "delivered"


class NewOrder(BaseModel):
    customer: str = Field(min_length=2, max_length=120)
    total: int = Field(gt=0)
    city: str | None = Field(default=None, max_length=50)
    note: str | None = Field(default=None, max_length=200)


class Order(BaseModel):
    id: str
    customer: str
    total: int
    city: str | None = None
    note: str | None = None
    status: OrderStatus


ORDERS = {
    "A101": Order(
        id="A101",
        customer="Noor Foods",
        total=4500,
        status=OrderStatus.PENDING,
    ),
    "A102": Order(
        id="A102",
        customer="Bilal Traders",
        total=12800,
        status=OrderStatus.DELIVERED,
    ),
    "A103": Order(
        id="A103",
        customer="Karachi Crafts",
        total=2300,
        status=OrderStatus.PENDING,
    ),
}


@app.get("/")
def read_root() -> dict[str, str]:
    return {"app": "Noor Foods Orders API", "docs": "/docs"}


@app.get("/orders")
def list_orders(status: OrderStatus | None = None, limit: int = 10) -> list[Order]:
    orders = []
    for order in ORDERS.values():
        if status is None or order.status == status:
            orders.append(order)
    return orders[:limit]


@app.get("/orders/{order_id}")
def get_order(order_id: str) -> Order:
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return ORDERS[order_id]


@app.post("/orders", status_code=201)
def create_order(new_order: NewOrder) -> Order:
    order_id = f"A{101 + len(ORDERS)}"
    order = Order(
        id=order_id,
        customer=new_order.customer,
        total=new_order.total,
        city=new_order.city,
        note=new_order.note,
        status=OrderStatus.PENDING,
    )
    ORDERS[order_id] = order
    return order


# problem 2 :
#  A delivery note: The response returns 422 Unprocessable Entity.
#  The loc is ["body", "note"], meaning the note field exceeds the 200-character limit.


# problem 3 :
#  Read the error: The response returns 422 Unprocessable Entity with two validation errors:
#  customer: string_too_short — customer name is empty; minimum 2 characters required.
#  total: int_parsing — "free" cannot be converted into an integer.
