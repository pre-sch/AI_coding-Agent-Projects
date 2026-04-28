import { Link, Route, Routes } from 'react-router-dom'
import { HomePage } from './pages/HomePage'
import { AboutPage } from './pages/AboutPage'
import { ContactPage } from './pages/ContactPage'
import { CatalogPage } from './pages/CatalogPage'
import { CartPage } from './pages/CartPage'
import { CheckoutPage } from './pages/CheckoutPage'
import { AdminDashboardPage } from './pages/AdminDashboardPage'

export default function App() {
  return (
    <div style={{ maxWidth: 960, margin: '0 auto', padding: 16 }}>
      <header>
        <h1>Business Commerce</h1>
        <nav style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          <Link to="/">Home</Link>
          <Link to="/about">About</Link>
          <Link to="/contact">Contact</Link>
          <Link to="/catalog">Catalog</Link>
          <Link to="/cart">Cart</Link>
          <Link to="/checkout">Checkout</Link>
          <Link to="/admin">Admin</Link>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/catalog" element={<CatalogPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/admin" element={<AdminDashboardPage />} />
        </Routes>
      </main>
    </div>
  )
}
