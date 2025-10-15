import { useState, useEffect } from 'react'
import axios from 'axios'
import Hero from './components/Hero'
import Header from './components/Header'
import ProductGrid from './components/ProductGrid'
import Cart from './components/Cart'
import Recommendations from './components/Recommendations'
import Chatbot from './components/Chatbot'
import InitialSetup from './components/InitialSetup'
import './App.css'

const API_BASE = 'http://localhost:8000'

function App() {
  const [showHero, setShowHero] = useState(true)
  const [products, setProducts] = useState([])
  const [cartItems, setCartItems] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [categories, setCategories] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [showCart, setShowCart] = useState(false)
  const [showChatbot, setShowChatbot] = useState(false)
  const [loading, setLoading] = useState(true)
  const [needsSetup, setNeedsSetup] = useState(false)

  // Fetch initial data
  useEffect(() => {
    fetchProducts()
    fetchCategories()
    fetchCart()
  }, [])

  // Fetch recommendations when cart changes
  useEffect(() => {
    if (cartItems.length > 0) {
      fetchRecommendations()
    }
  }, [cartItems])

  const fetchProducts = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_BASE}/api/products`)
      
      if (response.data.length === 0) {
        setNeedsSetup(true)
      } else {
        setProducts(response.data)
        setNeedsSetup(false)
      }
    } catch (error) {
      console.error('Error fetching products:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/categories`)
      setCategories(response.data)
    } catch (error) {
      console.error('Error fetching categories:', error)
    }
  }

  const fetchCart = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/cart`)
      setCartItems(response.data)
    } catch (error) {
      console.error('Error fetching cart:', error)
    }
  }

  const fetchRecommendations = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/recommendations`)
      setRecommendations(response.data)
    } catch (error) {
      console.error('Error fetching recommendations:', error)
    }
  }

  const handleAddToCart = async (productId) => {
    try {
      await axios.post(`${API_BASE}/api/cart`, {
        product_id: productId,
        quantity: 1
      })
      fetchCart()
    } catch (error) {
      console.error('Error adding to cart:', error)
    }
  }

  const handleUpdateQuantity = async (cartItemId, quantity) => {
    try {
      if (quantity <= 0) {
        await axios.delete(`${API_BASE}/api/cart/${cartItemId}`)
      } else {
        await axios.put(`${API_BASE}/api/cart/${cartItemId}?quantity=${quantity}`)
      }
      fetchCart()
    } catch (error) {
      console.error('Error updating cart:', error)
    }
  }

  const handleRemoveFromCart = async (cartItemId) => {
    try {
      await axios.delete(`${API_BASE}/api/cart/${cartItemId}`)
      fetchCart()
    } catch (error) {
      console.error('Error removing from cart:', error)
    }
  }

  const handleSetupComplete = () => {
    setNeedsSetup(false)
    fetchProducts()
  }

  const filteredProducts = products.filter(product => {
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesCategory && matchesSearch
  })

  const cartProductIds = cartItems.map(item => item.product_id)

  const handleStartShopping = () => {
    setShowHero(false)
    fetchProducts()
    fetchCategories()
    fetchCart()
  }

  const handleGoHome = () => {
    setShowHero(true)
  }

  if (showHero) {
    return <Hero onStartShopping={handleStartShopping} />
  }

  if (needsSetup) {
    return <InitialSetup onSetupComplete={handleSetupComplete} />
  }

  return (
    <div className="app">
      <Header 
        cartCount={cartItems.reduce((sum, item) => sum + item.quantity, 0)}
        onCartClick={() => setShowCart(!showCart)}
        onChatClick={() => setShowChatbot(!showChatbot)}
        onHomeClick={handleGoHome}
      />

      <main className="main-content">
        <div className="container">
          {/* Search and Filter */}
          <div className="controls">
            <input
              type="text"
              placeholder="Search products..."
              className="search-input"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />

            <div className="category-filters">
              <button
                className={`filter-btn ${selectedCategory === 'all' ? 'active' : ''}`}
                onClick={() => setSelectedCategory('all')}
              >
                All
              </button>
              {categories.map(category => (
                <button
                  key={category}
                  className={`filter-btn ${selectedCategory === category ? 'active' : ''}`}
                  onClick={() => setSelectedCategory(category)}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          {/* Recommendations Section */}
          {recommendations.length > 0 && (
            <Recommendations 
              recommendations={recommendations}
              onAddToCart={handleAddToCart}
              cartItems={cartItems}
            />
          )}

          {/* Products Grid */}
          {loading ? (
            <div className="spinner"></div>
          ) : (
            <ProductGrid 
              products={filteredProducts}
              onAddToCart={handleAddToCart}
              cartProductIds={cartProductIds}
            />
          )}
        </div>
      </main>

      {/* Cart Sidebar */}
      {showCart && (
        <Cart
          items={cartItems}
          onUpdateQuantity={handleUpdateQuantity}
          onRemove={handleRemoveFromCart}
          onClose={() => setShowCart(false)}
        />
      )}

      {/* Chatbot */}
      {showChatbot && (
        <Chatbot
          cartItems={cartItems}
          recommendations={recommendations}
          onClose={() => setShowChatbot(false)}
        />
      )}
    </div>
  )
}

export default App
