from fastapi import FastAPI
from .routers import products, orders

app = FastAPI()

app.include_router(products.router)
app.include_router(orders.router)