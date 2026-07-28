import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import './App.css'

export default function App() {
  const [activeSection, setActiveSection] = useState('home')
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "🍝 Benvenuti! Welcome to Bella Italia. I'm your reservation assistant. How can I help you book a table today?",
      sender: 'bot',
      timestamp: new Date()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  // Menu items
  const menu = {
    appetizers: [
      { name: "Bruschetta al Pomodoro", price: "$8", desc: "Toasted bread with fresh tomatoes and basil" },
      { name: "Calamari Fritti", price: "$12", desc: "Golden fried squid with marinara sauce" },
      { name: "Mozzarella di Bufala", price: "$10", desc: "Fresh buffalo mozzarella with heirloom tomatoes" }
    ],
    pasta: [
      { name: "Spaghetti al Carbonara", price: "$16", desc: "Classic Roman pasta with eggs, guanciale, and cheese" },
      { name: "Pappardelle al Ragù", price: "$18", desc: "Wide ribbon pasta with slow-cooked meat sauce" },
      { name: "Lasagna della Nonna", price: "$15", desc: "Traditional layered pasta with bolognese and béchamel" },
      { name: "Osso Buco with Risotto", price: "$28", desc: "Braised veal shanks served with saffron risotto" }
    ],
    pizza: [
      { name: "Margherita", price: "$14", desc: "Classic tomato, mozzarella, and basil" },
      { name: "Quattro Formaggi", price: "$16", desc: "Four cheese blend with truffle oil" },
      { name: "Prosciutto e Rucola", price: "$17", desc: "Thin crust with prosciutto and arugula" }
    ],
    desserts: [
      { name: "Tiramisu", price: "$7", desc: "Layers of mascarpone, espresso, and cocoa" },
      { name: "Panna Cotta", price: "$7", desc: "Silky vanilla cream with berry compote" },
      { name: "Gelato Trio", price: "$8", desc: "Three flavors of authentic Italian gelato" }
    ]
  }

  // API base URL: set VITE_API_URL=/api in Vercel env vars; empty = localhost for local dev
  const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000') + '/chat'

  // Auto-scroll to latest message
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Handle sending message
  const handleSendMessage = async (e) => {
    e.preventDefault()

    if (!inputValue.trim()) return

    // Add user message to chat
    const userMessage = {
      id: messages.length + 1,
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages([...messages, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      // Send to backend
      const response = await axios.post(API_URL, {
        message: inputValue
      })

      // Add bot response
      const botMessage = {
        id: messages.length + 2,
        text: response.data.reply,
        sender: 'bot',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error:', error)

      // Add error message
      const errorMessage = {
        id: messages.length + 2,
        text: `Error: ${error.response?.data?.detail || error.message || 'Unable to connect to server. Make sure the backend is running.'}`,
        sender: 'bot',
        timestamp: new Date(),
        isError: true
      }

      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app-wrapper">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="logo">
            🍝 <span className="restaurant-name">Bella Italia</span>
          </div>
          <ul className="nav-menu">
            <li><button className={`nav-btn ${activeSection === 'home' ? 'active' : ''}`} onClick={() => setActiveSection('home')}>Home</button></li>
            <li><button className={`nav-btn ${activeSection === 'menu' ? 'active' : ''}`} onClick={() => setActiveSection('menu')}>Menu</button></li>
            <li><button className={`nav-btn ${activeSection === 'about' ? 'active' : ''}`} onClick={() => setActiveSection('about')}>About</button></li>
            <li><button className={`nav-btn ${activeSection === 'reserve' ? 'active' : ''}`} onClick={() => setActiveSection('reserve')}>Reserve</button></li>
          </ul>
        </div>
      </nav>

      {/* Main Content */}
      <div className="main-content">
        {/* HOME SECTION */}
        {activeSection === 'home' && (
          <div className="section home-section">
            <div className="hero">
              <div className="hero-content">
                <h1 className="hero-title">Bella Italia</h1>
                <p className="hero-subtitle">Authentic Italian Cuisine • Family Recipes Since 1995</p>
                <p className="hero-description">Experience the warmth and flavors of Italy in every dish</p>
                <button className="cta-button" onClick={() => setActiveSection('reserve')}>
                  🍷 Book a Table
                </button>
              </div>
            </div>

            <div className="info-section">
              <div className="info-card">
                <div className="info-icon">🕐</div>
                <h3>Hours</h3>
                <p>Monday - Sunday</p>
                <p className="info-highlight">11:00 AM - 10:00 PM</p>
              </div>
              <div className="info-card">
                <div className="info-icon">📍</div>
                <h3>Location</h3>
                <p>123 Italian Street</p>
                <p className="info-highlight">New York, NY 10001</p>
              </div>
              <div className="info-card">
                <div className="info-icon">📞</div>
                <h3>Contact</h3>
                <p>(555) 123-4567</p>
                <p className="info-highlight">info@bellaitalia.com</p>
              </div>
            </div>
          </div>
        )}

        {/* MENU SECTION */}
        {activeSection === 'menu' && (
          <div className="section menu-section">
            <h2 className="section-title">🍽️ Our Menu</h2>
            
            <div className="menu-container">
              <div className="menu-category">
                <h3>Appetizers (Antipasti)</h3>
                {menu.appetizers.map((item, idx) => (
                  <div key={idx} className="menu-item">
                    <div className="menu-item-header">
                      <span className="menu-item-name">{item.name}</span>
                      <span className="menu-item-price">{item.price}</span>
                    </div>
                    <p className="menu-item-desc">{item.desc}</p>
                  </div>
                ))}
              </div>

              <div className="menu-category">
                <h3>Pasta & Risotto</h3>
                {menu.pasta.map((item, idx) => (
                  <div key={idx} className="menu-item">
                    <div className="menu-item-header">
                      <span className="menu-item-name">{item.name}</span>
                      <span className="menu-item-price">{item.price}</span>
                    </div>
                    <p className="menu-item-desc">{item.desc}</p>
                  </div>
                ))}
              </div>

              <div className="menu-category">
                <h3>Pizza (Pizzas)</h3>
                {menu.pizza.map((item, idx) => (
                  <div key={idx} className="menu-item">
                    <div className="menu-item-header">
                      <span className="menu-item-name">{item.name}</span>
                      <span className="menu-item-price">{item.price}</span>
                    </div>
                    <p className="menu-item-desc">{item.desc}</p>
                  </div>
                ))}
              </div>

              <div className="menu-category">
                <h3>Desserts (Dolci)</h3>
                {menu.desserts.map((item, idx) => (
                  <div key={idx} className="menu-item">
                    <div className="menu-item-header">
                      <span className="menu-item-name">{item.name}</span>
                      <span className="menu-item-price">{item.price}</span>
                    </div>
                    <p className="menu-item-desc">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ABOUT SECTION */}
        {activeSection === 'about' && (
          <div className="section about-section">
            <h2 className="section-title">About Bella Italia</h2>
            <div className="about-content">
              <div className="about-text">
                <h3>Our Story</h3>
                <p>
                  Founded in 1995 by the Rossi family, Bella Italia has been serving authentic Italian cuisine to the New York community for over 25 years. Every recipe is passed down through generations, using only the finest imported ingredients from Italy.
                </p>
                <p>
                  We believe in the Italian philosophy of "mangiare bene, vivere bene" – to eat well is to live well. Our chefs prepare each dish with passion and care, ensuring that every meal is a celebration of Italian culture and tradition.
                </p>
                <h3>Our Commitment</h3>
                <ul className="values-list">
                  <li>✓ Fresh, imported ingredients from Italy</li>
                  <li>✓ Traditional recipes prepared by Italian chefs</li>
                  <li>✓ Warm hospitality and family atmosphere</li>
                  <li>✓ Local, seasonal produce when available</li>
                  <li>✓ Wine selection featuring Italian vineyards</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* RESERVATION SECTION */}
        {activeSection === 'reserve' && (
          <div className="section reserve-section">
            <h2 className="section-title">📅 Make a Reservation</h2>
            <div className="chat-wrapper">
              <div className="chat-container">
                <div className="messages-container">
                  {messages.map((msg) => (
                    <div key={msg.id} className={`message ${msg.sender} ${msg.isError ? 'error' : ''}`}>
                      <div className="message-content">
                        {msg.text}
                      </div>
                      <div className="message-time">
                        {msg.timestamp.toLocaleTimeString([], {
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="message bot loading">
                      <div className="message-content">
                        <span className="typing-indicator">
                          <span></span>
                          <span></span>
                          <span></span>
                        </span>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>

                <form className="input-container" onSubmit={handleSendMessage}>
                  <input
                    type="text"
                    placeholder="Tell me about your reservation needs..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    disabled={isLoading}
                    className="chat-input"
                  />
                  <button
                    type="submit"
                    disabled={isLoading || !inputValue.trim()}
                    className="send-button"
                  >
                    Send
                  </button>
                </form>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <p>&copy; 2024 Bella Italia Ristorante. All rights reserved. | Buon Appetito! 🍝</p>
        </div>
      </footer>
    </div>
  )
}
