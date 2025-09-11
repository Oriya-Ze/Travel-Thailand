from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductOut
from app.deps.auth import require_role


router = APIRouter(prefix="/products", tags=["catalog"])


@router.post("", response_model=ProductOut, dependencies=[Depends(require_role({"admin"}))])
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    obj = Product(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    obj = db.get(Product, product_id)
    if not obj:
        raise HTTPException(404, "Product not found")
    return obj
