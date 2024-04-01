from fastapi import APIRouter, Depends, HTTPException, HTTPStatus
from sqlalchemy.orm import Session
from .. import crud, schemas, dependencies, auth
from ..auth import get_current_user

router = APIRouter()

@router.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(dependencies.get_db), current_user: auth.ShopifyStore = Depends(get_current_user)):
    return crud.create_order(db=db, order=order)

@router.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db), current_user: auth.ShopifyStore = Depends(get_current_user)):
    return crud.get_orders(db, skip=skip, limit=limit)

@router.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(dependencies.get_db), current_user: auth.ShopifyStore = Depends(get_current_user)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")
    return db_order

@router.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderCreate, db: Session = Depends(dependencies.get_db), current_user: auth.ShopifyStore = Depends(get_current_user)):
    return crud.update_order(db, order_id, order)

@router.delete("/orders/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(dependencies.get_db), current_user: auth.ShopifyStore = Depends(get_current_user)):
    return crud.delete_order(db, order_id)
