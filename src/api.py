from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

orders_db = {}
next_id = 1


class OrderCreate(BaseModel):
    customer_name: str


class OrderOut(BaseModel):
    id: int
    customer_name: str
    status: str


@app.post("/orders", response_model=OrderOut)
def create_order(order: OrderCreate):
    global next_id
    order_id = next_id
    next_id += 1
    orders_db[order_id] = {
        "id": order_id,
        "customer_name": order.customer_name,
        "status": "created",
    }
    return orders_db[order_id]


@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]