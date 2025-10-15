import { useState } from 'react'
import axios from 'axios'
import './InitialSetup.css'

const API_BASE = 'http://localhost:8000'

function InitialSetup({ onSetupComplete }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [count, setCount] = useState(50)

  const handleGenerate = async () => {
    setLoading(true)
    setError('')

    try {
      const response = await axios.post(`${API_BASE}/api/products/generate?count=${count}`)
      console.log(response.data)
      
      // Wait a moment for database to be ready
      setTimeout(() => {
        onSetupComplete()
      }, 500)
    } catch (err) {
      console.error('Error generating products:', err)
      setError(err.response?.data?.detail || 'Failed to generate products. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div className="setup-container">
      <div className="setup-card">
        <div className="earth-container">
          <div className="earth">
            <div className="earth-sphere">
              <div className="continent continent-1"></div>
              <div className="continent continent-2"></div>
              <div className="continent continent-3"></div>
              <div className="continent continent-4"></div>
              <div className="continent continent-5"></div>
            </div>
            <div className="earth-glow"></div>
          </div>
        </div>
        <h1>Welcome to ShopSmart!</h1>
        <p className="setup-subtitle">AI-Powered E-Commerce Recommender</p>

        <div className="setup-content">
          <h2>🚀 Initial Setup Required</h2>
          <p>
            Before you can start shopping, we need to generate a product catalog using
            Google Gemini AI. This will create realistic grocery products for you to browse.
          </p>

          <div className="setup-options">
            <label>
              <span>Number of products to generate:</span>
              <input
                type="number"
                min="10"
                max="100"
                value={count}
                onChange={(e) => setCount(parseInt(e.target.value))}
                disabled={loading}
              />
            </label>
          </div>

          <div className="setup-features">
            <h3>✨ What you'll get:</h3>
            <ul>
              <li>🍎 Diverse product catalog (Fruits, Dairy, Snacks, etc.)</li>
              <li>🤖 AI-powered product recommendations</li>
              <li>💬 Smart chatbot to explain recommendations</li>
              <li>🛒 Full shopping cart functionality</li>
            </ul>
          </div>

          {error && (
            <div className="setup-error">
              ⚠️ {error}
            </div>
          )}

          <button
            className="setup-btn"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? (
              <>
                <div className="btn-spinner"></div>
                Generating Products...
              </>
            ) : (
              '🎉 Generate Products & Start Shopping'
            )}
          </button>

          <p className="setup-note">
            <strong>Note:</strong> Make sure you have configured your Gemini API key in the backend .env file
          </p>
        </div>
      </div>
    </div>
  )
}

export default InitialSetup
