from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, dependencies

router = APIRouter()

@router.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_product(db=db, product=product)

@router.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(dependencies.get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(dependencies.get_db)):
    db_product = crud.update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(dependencies.get_db)):
    db_product = crud.delete_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
