import { useState } from 'react'
import './Recommendations.css'

function Recommendations({ recommendations, onAddToCart, cartItems }) {
  const [showExplanation, setShowExplanation] = useState({})

  if (recommendations.length === 0) return null

  const toggleExplanation = (idx) => {
    setShowExplanation(prev => ({
      ...prev,
      [idx]: !prev[idx]
    }))
  }

  const getCartSummary = () => {
    return cartItems.map(item => item.product.name).join(', ')
  }

  return (
    <div className="recommendations-section">
      <div className="recommendations-header">
        <h2>🎯 Recommended for You</h2>
        <p>AI-powered suggestions based on your cart</p>
      </div>

      <div className="recommendations-grid">
        {recommendations.map((rec, idx) => (
          <div key={idx} className="recommendation-card">
            <div className="rec-badge">
              <span>AI Recommended</span>
              <span className="score">{Math.round(rec.score * 100)}% match</span>
            </div>

            <div className="rec-image">
              <img 
                src={rec.product.image_url} 
                alt={rec.product.name}
                onError={(e) => {
                  e.target.src = `https://placehold.co/300x300/667eea/white/png?text=${encodeURIComponent(rec.product.name)}`
                }}
              />
            </div>

            <div className="rec-content">
              <h3>{rec.product.name}</h3>
              <p className="rec-category">{rec.product.category}</p>
              
              <div className="rec-reason">
                <span className="reason-icon">💡</span>
                <p>{rec.reason}</p>
              </div>

              {showExplanation[idx] && (
                <div className="rec-detailed-explanation">
                  <div className="explanation-header">
                    <span className="explanation-icon">🎯</span>
                    <h4>Why This Recommendation?</h4>
                  </div>
                  
                  <div className="explanation-content">
                    <div className="explanation-row">
                      <strong>Your Cart:</strong>
                      <span className="cart-summary">{getCartSummary()}</span>
                    </div>

                    <div className="explanation-row highlight">
                      <strong>Perfect Match:</strong>
                      <span>{rec.reason}</span>
                    </div>

                    <div className="confidence-mini">
                      <span className="confidence-label">AI Confidence:</span>
                      <div className="confidence-bar-mini">
                        <div 
                          className="confidence-fill-mini" 
                          style={{ width: `${rec.score * 100}%` }}
                        ></div>
                      </div>
                      <span className="confidence-percent">{Math.round(rec.score * 100)}%</span>
                    </div>

                    <p className="cta-mini">💡 Complete your shopping - Add to cart now!</p>
                  </div>
                </div>
              )}

              <div className="rec-footer">
                <span className="rec-price">${rec.product.price.toFixed(2)}</span>
                <div className="rec-actions">
                  <button
                    className={`why-btn ${showExplanation[idx] ? 'active' : ''}`}
                    onClick={() => toggleExplanation(idx)}
                    title="See detailed explanation"
                  >
                    {showExplanation[idx] ? '✓ Got it!' : '❓ Why?'}
                  </button>
                  <button
                    className="add-rec-btn"
                    onClick={() => onAddToCart(rec.product.id)}
                  >
                    + Add
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Recommendations
