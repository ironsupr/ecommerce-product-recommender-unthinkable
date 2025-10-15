import './Header.css'

function Header({ cartCount, onCartClick, onChatClick, onHomeClick }) {
  return (
    <header className="header">
      <div className="container header-container">
        <div className="logo" onClick={onHomeClick} style={{ cursor: 'pointer' }}>
          <h1>🛒 ShopMart</h1>
          <span className="tagline">AI-Powered Shopping</span>
        </div>

        <div className="header-actions">
          <button className="chat-btn" onClick={onChatClick}>
            💬 Ask AI
          </button>
          
          <button className="cart-btn" onClick={onCartClick}>
            🛒 Cart
            {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
