import { useState } from 'react'
import axios from 'axios'
import './Chatbot.css'

function Chatbot({ cartItems, recommendations, onClose }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hi! I'm your AI shopping assistant. 🛒\n\nI can help you:\n• Understand why products are recommended\n• Find items that go well together\n• Get shopping advice\n\nWhat would you like to know?"
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const quickQuestions = [
    "Why was this product recommended?",
    "What goes well with items in my cart?",
    "Tell me more about the recommendations",
    "Are these products healthy?"
  ]

  const handleSend = async (question = input) => {
    if (!question.trim()) return

    const userMessage = { role: 'user', content: question }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const cartProductIds = cartItems.map(item => item.product_id)
      const recommendedProductId = recommendations.length > 0 ? recommendations[0].product.id : null

      console.log('Sending chat request:', { question, cartProductIds, recommendedProductId })

      const response = await axios.post('/api/chat', {
        question,
        cart_items: cartProductIds,
        recommended_product_id: recommendedProductId
      })

      console.log('Chat response:', response.data)

      const assistantMessage = { role: 'assistant', content: response.data.answer }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      console.error('Error details:', error.response?.data || error.message)
      const errorMessage = {
        role: 'assistant',
        content: `Sorry, I'm having trouble processing your question. ${error.response?.data?.detail || 'Please try again.'}`
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <>
      <div className="chatbot-overlay" onClick={onClose}></div>
      <div className="chatbot-container">
        <div className="chatbot-header">
          <div>
            <h3>🤖 AI Shopping Assistant</h3>
            <p>Ask me anything!</p>
          </div>
          <button className="chatbot-close" onClick={onClose}>✕</button>
        </div>

        <div className="chatbot-messages">
          {messages.map((message, idx) => (
            <div key={idx} className={`message ${message.role}`}>
              <div className="message-avatar">
                {message.role === 'assistant' ? '🤖' : '👤'}
              </div>
              <div className="message-content">
                <p>{message.content}</p>
              </div>
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
        </div>

        {messages.length === 1 && (
          <div className="quick-questions">
            <p className="quick-label">Quick questions:</p>
            {quickQuestions.map((q, idx) => (
              <button
                key={idx}
                className="quick-btn"
                onClick={() => handleSend(q)}
              >
                {q}
              </button>
            ))}
          </div>
        )}

        <div className="chatbot-input">
          <input
            type="text"
            placeholder="Ask about recommendations..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
          />
          <button onClick={() => handleSend()} disabled={loading || !input.trim()}>
            Send
          </button>
        </div>
      </div>
    </>
  )
}

export default Chatbot
