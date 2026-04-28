import { useEffect, useState } from 'react'
import { api } from '../api/client'

type Product = { id: number; name: string; price: string; description: string }

export function CatalogPage() {
  const [products, setProducts] = useState<Product[]>([])

  useEffect(() => {
    api.get('/products/').then((res) => setProducts(res.data.results ?? res.data)).catch(() => setProducts([]))
  }, [])

  return <section><h2>Catalog</h2>{products.map((p) => <article key={p.id}><h3>{p.name}</h3><p>${p.price}</p><p>{p.description}</p></article>)}</section>
}
