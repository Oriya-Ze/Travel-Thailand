from pydantic import BaseModel


class ProductCreate(BaseModel):
    title: str
    brand: str | None = None
    category_id: int | None = None
    specs: dict | None = None
    price: float
    stock: int = 0


class ProductOut(ProductCreate):
    id: int
    class Config:
        from_attributes = True
