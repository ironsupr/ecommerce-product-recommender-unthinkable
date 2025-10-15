from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json

from database import get_db, init_db, Product, CartItem, UserInteraction
from models import (
    ProductResponse, CartItemCreate, CartItemResponse, CartItemWithProduct,
    RecommendationResponse, ChatRequest, ChatResponse
)
from gemini_service import generate_synthetic_products, get_recommendations, answer_question

app = FastAPI(
    title="E-Commerce Product Recommender API",
    description="AI-powered product recommendation system using Google Gemini",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    return {
        "message": "E-Commerce Product Recommender API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.post("/api/products/generate")
async def generate_products(count: int = 50, db: Session = Depends(get_db)):
    """Generate synthetic products using Gemini and store in database"""
    
    # Check if products already exist
    existing_count = db.query(Product).count()
    if existing_count > 0:
        raise HTTPException(status_code=400, detail=f"Products already exist ({existing_count} products). Clear database first.")
    
    # Generate products using Gemini
    products_data = await generate_synthetic_products(count)
    
    # Store in database
    for product_data in products_data:
        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            category=product_data['category'],
            price=product_data['price'],
            image_url=product_data['image_url'],
            tags=product_data['tags']
        )
        db.add(product)
    
    db.commit()
    
    return {
        "message": f"Successfully generated {len(products_data)} products",
        "count": len(products_data)
    }


@app.get("/api/products", response_model=List[ProductResponse])
async def get_products(
    category: str = None,
    search: str = None,
    db: Session = Depends(get_db)
):
    """Get all products with optional filtering"""
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    
    if search:
        query = query.filter(
            (Product.name.contains(search)) | 
            (Product.description.contains(search))
        )
    
    products = query.all()
    return products


@app.get("/api/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Log interaction
    interaction = UserInteraction(product_id=product_id, interaction_type="view")
    db.add(interaction)
    db.commit()
    
    return product


@app.get("/api/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get all unique product categories"""
    categories = db.query(Product.category).distinct().all()
    return [cat[0] for cat in categories]


@app.get("/api/cart", response_model=List[CartItemWithProduct])
async def get_cart(db: Session = Depends(get_db)):
    """Get all items in cart with product details"""
    cart_items = db.query(CartItem).all()
    
    result = []
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            result.append({
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "added_at": item.added_at,
                "product": product
            })
    
    return result


@app.post("/api/cart", response_model=CartItemResponse)
async def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):
    """Add item to cart"""
    
    # Check if product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if item already in cart
    existing_item = db.query(CartItem).filter(CartItem.product_id == item.product_id).first()
    
    if existing_item:
        existing_item.quantity += item.quantity
        db.commit()
        db.refresh(existing_item)
        cart_item = existing_item
    else:
        cart_item = CartItem(
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
    
    # Log interaction
    interaction = UserInteraction(product_id=item.product_id, interaction_type="add_to_cart")
    db.add(interaction)
    db.commit()
    
    return cart_item


@app.put("/api/cart/{cart_item_id}")
async def update_cart_item(cart_item_id: int, quantity: int, db: Session = Depends(get_db)):
    """Update cart item quantity"""
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    if quantity <= 0:
        db.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.commit()
    
    return {"message": "Cart updated successfully"}


@app.delete("/api/cart/{cart_item_id}")
async def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db)):
    """Remove item from cart"""
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    
    return {"message": "Item removed from cart"}


@app.delete("/api/cart")
async def clear_cart(db: Session = Depends(get_db)):
    """Clear all items from cart"""
    db.query(CartItem).delete()
    db.commit()
    
    return {"message": "Cart cleared successfully"}


@app.get("/api/recommendations", response_model=List[RecommendationResponse])
async def get_product_recommendations(db: Session = Depends(get_db)):
    """Get AI-powered product recommendations based on cart"""
    
    # Get cart items
    cart_items = db.query(CartItem).all()
    cart_product_ids = [item.product_id for item in cart_items]
    
    # Get cart products
    cart_products = []
    for product_id in cart_product_ids:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            cart_products.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "image_url": product.image_url,
                "tags": product.tags
            })
    
    # Get all products for recommendations
    all_products_db = db.query(Product).filter(~Product.id.in_(cart_product_ids)).all()
    all_products = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "category": p.category,
            "price": p.price,
            "image_url": p.image_url,
            "tags": p.tags
        }
        for p in all_products_db
    ]
    
    # Get recommendations from Gemini
    recommendations = await get_recommendations(cart_products, all_products)
    
    return recommendations


@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest, db: Session = Depends(get_db)):
    """Chat with AI assistant about recommendations"""
    
    # Get cart products
    cart_products = []
    for product_id in request.cart_items:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            cart_products.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "tags": product.tags
            })
    
    # Get recommended product if provided
    recommended_product = None
    if request.recommended_product_id:
        product = db.query(Product).filter(Product.id == request.recommended_product_id).first()
        if product:
            recommended_product = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "tags": product.tags
            }
    
    # Get answer from Gemini
    answer = await answer_question(request.question, cart_products, recommended_product)
    
    return ChatResponse(answer=answer)


@app.delete("/api/products/clear")
async def clear_products(db: Session = Depends(get_db)):
    """Clear all products from database (for testing)"""
    db.query(CartItem).delete()
    db.query(UserInteraction).delete()
    db.query(Product).delete()
    db.commit()
    
    return {"message": "All products cleared"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
