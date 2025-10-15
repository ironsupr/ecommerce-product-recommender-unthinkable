from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    price: float
    image_url: str
    tags: str


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    
    class Config:
        from_attributes = True


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemResponse(CartItemBase):
    id: int
    added_at: datetime
    
    class Config:
        from_attributes = True


class CartItemWithProduct(BaseModel):
    id: int
    product_id: int
    quantity: int
    added_at: datetime
    product: ProductResponse
    
    class Config:
        from_attributes = True


class RecommendationRequest(BaseModel):
    cart_items: List[int]  # List of product IDs in cart


class RecommendationResponse(BaseModel):
    product: ProductResponse
    reason: str
    score: float


class ChatRequest(BaseModel):
    question: str
    cart_items: Optional[List[int]] = []
    recommended_product_id: Optional[int] = None


class ChatResponse(BaseModel):
    answer: str
