import './Hero.css'

function Hero({ onStartShopping }) {
  return (
    <div className="hero-container">
      <div className="hero-content">
        <div className="hero-text">
          <h1 className="hero-title">
            <span className="title-main">ShopMart</span>
            <span className="title-sub">AI-Powered Shopping</span>
          </h1>
          
          <div className="punchline">
            <span className="punchline-text">
              ✨ Discover. Shop. Experience.
            </span>
          </div>

          <p className="hero-description">
            Experience the future of e-commerce with AI-driven recommendations
            tailored just for you. Shop smarter, not harder.
          </p>

          <div className="hero-features">
            <div className="feature">
              <span className="feature-icon">🤖</span>
              <span>AI Recommendations</span>
            </div>
            <div className="feature">
              <span className="feature-icon">⚡</span>
              <span>Lightning Fast</span>
            </div>
            <div className="feature">
              <span className="feature-icon">🎯</span>
              <span>Personalized</span>
            </div>
          </div>

          <button className="hero-cta" onClick={onStartShopping}>
            Start Shopping
            <span className="cta-arrow">→</span>
          </button>
        </div>

        <div className="hero-globe">
          <div className="cube-container">
            <div className="cube">
              <div className="cube-face front">🛒</div>
              <div className="cube-face back">🎁</div>
              <div className="cube-face right">⚡</div>
              <div className="cube-face left">🤖</div>
              <div className="cube-face top">✨</div>
              <div className="cube-face bottom">🎯</div>
            </div>
            <div className="orbit-ring ring-1"></div>
            <div className="orbit-ring ring-2"></div>
            <div className="orbit-ring ring-3"></div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Hero
