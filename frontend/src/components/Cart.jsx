import './Cart.css'

function Cart({ items, onUpdateQuantity, onRemove, onClose }) {
  const total = items.reduce((sum, item) => sum + (item.product.price * item.quantity), 0)

  return (
    <>
      <div className="cart-overlay" onClick={onClose}></div>
      <div className="cart-sidebar">
        <div className="cart-header">
          <h2>Your Cart ({items.length})</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="cart-items">
          {items.length === 0 ? (
            <div className="empty-cart">
              <p>🛒</p>
              <h3>Your cart is empty</h3>
              <p>Add some products to get started!</p>
            </div>
          ) : (
            items.map(item => (
              <div key={item.id} className="cart-item">
                <img 
                  src={item.product.image_url} 
                  alt={item.product.name}
                  onError={(e) => {
                    e.target.src = `https://placehold.co/300x300/667eea/white/png?text=${encodeURIComponent(item.product.name)}`
                  }}
                />
                
                <div className="cart-item-info">
                  <h4>{item.product.name}</h4>
                  <p className="cart-item-category">{item.product.category}</p>
                  <p className="cart-item-price">${item.product.price.toFixed(2)}</p>
                </div>

                <div className="cart-item-actions">
                  <div className="quantity-controls">
                    <button onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}>-</button>
                    <span>{item.quantity}</span>
                    <button onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}>+</button>
                  </div>
                  
                  <button className="remove-btn" onClick={() => onRemove(item.id)}>
                    🗑️
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        {items.length > 0 && (
          <div className="cart-footer">
            <div className="cart-total">
              <span>Total:</span>
              <span className="total-amount">${total.toFixed(2)}</span>
            </div>
            <button className="checkout-btn">Proceed to Checkout</button>
          </div>
        )}
      </div>
    </>
  )
}

export default Cart
