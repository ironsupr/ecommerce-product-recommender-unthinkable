import './ProductGrid.css'

function ProductGrid({ products, onAddToCart, cartProductIds }) {
  if (products.length === 0) {
    return (
      <div className="empty-state">
        <h2>No products found</h2>
        <p>Try adjusting your search or filters</p>
      </div>
    )
  }

  return (
    <div className="product-grid">
      {products.map(product => (
        <div key={product.id} className="product-card">
          <div className="product-image">
            <img 
              src={product.image_url} 
              alt={product.name}
              onError={(e) => {
                e.target.src = `https://placehold.co/300x300/667eea/white/png?text=${encodeURIComponent(product.name)}`
              }}
            />
            <div className="product-tags">
              {product.tags.split(',').slice(0, 2).map((tag, idx) => (
                <span key={idx} className="tag">{tag.trim()}</span>
              ))}
            </div>
          </div>

          <div className="product-info">
            <h3 className="product-name">{product.name}</h3>
            <p className="product-category">{product.category}</p>
            <p className="product-description">{product.description.substring(0, 80)}...</p>
            
            <div className="product-footer">
              <span className="product-price">${product.price.toFixed(2)}</span>
              
              <button
                className={`add-btn ${cartProductIds.includes(product.id) ? 'in-cart' : ''}`}
                onClick={() => onAddToCart(product.id)}
                disabled={cartProductIds.includes(product.id)}
              >
                {cartProductIds.includes(product.id) ? '✓ In Cart' : '+ Add'}
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ProductGrid
