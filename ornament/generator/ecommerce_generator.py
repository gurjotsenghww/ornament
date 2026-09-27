from pathlib import Path
from typing import Dict, Any
from ornament.files.file_manager import FileManager

class EcommerceGenerator:
    """
    Scaffolds production-grade Next.js + React + TypeScript + Tailwind E-Commerce websites (Section 21).
    Capabilities: Catalog, product cards, product detail, filters, search, cart, checkout UI.
    """

    @classmethod
    def generate(cls, workspace_path: Path) -> Dict[str, Any]:
        fm = FileManager(workspace_path)

        # 1. package.json
        package_json = """{
  "name": "ornament-ecommerce-store",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.2.3",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "lucide-react": "^0.378.0"
  },
  "devDependencies": {
    "@types/node": "^20.12.7",
    "@types/react": "^18.3.1",
    "@types/react-dom": "^18.3.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.4.5"
  }
}
"""
        fm.create_file("package.json", package_json, overwrite=True)

        # 2. tsconfig.json
        tsconfig_json = """{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{"name": "next"}],
    "paths": {"@/*": ["./*"]}
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""
        fm.create_file("tsconfig.json", tsconfig_json, overwrite=True)

        # 3. tailwind.config.js
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "#09090b",
        surface: "#18181b",
        border: "#27272a",
        accent: "#10b981"
      }
    },
  },
  plugins: [],
}
"""
        fm.create_file("tailwind.config.js", tailwind_config, overwrite=True)

        # 4. app/globals.css
        globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root { color-scheme: dark; }
body { background-color: #09090b; color: #f4f4f5; margin: 0; }
"""
        fm.create_file("app/globals.css", globals_css, overwrite=True)

        # 5. components/StoreNavbar.tsx
        navbar_tsx = """import React from "react";

export default function StoreNavbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-zinc-800 bg-[#09090b]/85 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <a href="/" className="font-extrabold text-xl tracking-tight text-white flex items-center space-x-2">
          <span className="w-6 h-6 rounded bg-emerald-500 flex items-center justify-center text-xs font-black text-black">O</span>
          <span>AURA<span className="text-emerald-400">STORE</span></span>
        </a>
        <nav aria-label="Store Navigation" className="hidden md:flex items-center space-x-8 text-sm font-medium">
          <a href="/catalog" className="text-zinc-300 hover:text-white transition">Catalog</a>
          <a href="/catalog?category=hardware" className="text-zinc-300 hover:text-white transition">Hardware</a>
          <a href="/catalog?category=gear" className="text-zinc-300 hover:text-white transition">Developer Gear</a>
        </nav>
        <div className="flex items-center space-x-4">
          <a
            id="nav-cart-button"
            href="/checkout"
            className="px-4 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-sm font-medium text-white flex items-center space-x-2 border border-zinc-700"
          >
            <span>Cart</span>
            <span className="px-2 py-0.5 rounded-full bg-emerald-500 text-black text-xs font-bold">2</span>
          </a>
        </div>
      </div>
    </header>
  );
}
"""
        fm.create_file("components/StoreNavbar.tsx", navbar_tsx, overwrite=True)

        # 6. app/layout.tsx
        layout_tsx = """import "./globals.css";
import React from "react";
import StoreNavbar from "@/components/StoreNavbar";

export const metadata = {
  title: "AURA Store | Premium Autonomous Developer Hardware & Gear",
  description: "Next-generation developer setups, edge compute clusters, and precision ergonomics.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen flex flex-col bg-background text-zinc-100 antialiased">
        <StoreNavbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
"""
        fm.create_file("app/layout.tsx", layout_tsx, overwrite=True)

        # 7. components/ProductCard.tsx
        product_card_tsx = """import React from "react";

export interface Product {
  id: string;
  name: string;
  category: string;
  price: number;
  rating: number;
  description: string;
  inStock: boolean;
}

export default function ProductCard({ product }: { product: Product }) {
  return (
    <div className="group rounded-xl border border-zinc-800 bg-zinc-900/60 p-5 hover:border-emerald-500/50 transition-all flex flex-col justify-between">
      <div>
        <div className="h-44 rounded-lg bg-zinc-800/80 flex items-center justify-center text-zinc-500 font-mono text-sm mb-4 border border-zinc-700/50">
          [{product.category.toUpperCase()}]
        </div>
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs uppercase font-mono tracking-wider text-emerald-400">{product.category}</span>
          <span className="text-xs text-zinc-400">★ {product.rating}</span>
        </div>
        <h3 className="font-bold text-white text-lg group-hover:text-emerald-300 transition">{product.name}</h3>
        <p className="text-xs text-zinc-400 mt-2 line-clamp-2 leading-relaxed">{product.description}</p>
      </div>
      <div className="mt-6 flex items-center justify-between pt-4 border-t border-zinc-800">
        <span className="text-xl font-bold text-white">${product.price}</span>
        <a
          href={`/checkout?item=${product.id}`}
          className="px-3.5 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-black text-sm font-semibold transition"
        >
          Buy Now
        </a>
      </div>
    </div>
  );
}
"""
        fm.create_file("components/ProductCard.tsx", product_card_tsx, overwrite=True)

        # 8. app/page.tsx (Store Front Home)
        store_home_tsx = """import React from "react";
import ProductCard, { Product } from "@/components/ProductCard";

const FEATURED_PRODUCTS: Product[] = [
  {
    id: "prod-1",
    name: "Ornàment Edge Neural Node 64GB",
    category: "hardware",
    price: 899,
    rating: 4.9,
    description: "Local-first LLM inference workstation with silent dual fan cooling and high bandwidth memory.",
    inStock: true
  },
  {
    id: "prod-2",
    name: "Precision Split Mechanical Keyboard",
    category: "gear",
    price: 249,
    rating: 4.8,
    description: "Custom hot-swap switches with column-staggered layout and integrated OLED status display.",
    inStock: true
  },
  {
    id: "prod-3",
    name: "Thunderbolt 4 Ultra-Dock Dual 4K",
    category: "hardware",
    price: 189,
    rating: 4.7,
    description: "Single-cable connectivity providing 100W PD charging, 10Gbps Ethernet, and dual display outputs.",
    inStock: true
  }
];

export default function StoreHomePage() {
  return (
    <div className="space-y-12">
      <section className="py-12 sm:py-16 text-center max-w-3xl mx-auto">
        <span className="px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
          Engineered for Deep Work
        </span>
        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white mt-6">
          Hardware and tools for the local-first AI era.
        </h1>
        <p className="mt-4 text-zinc-400 text-lg">
          High-performance workstations, custom keyboards, and edge compute clusters built for software craftspeople.
        </p>
      </section>

      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-white">Featured Hardware</h2>
          <a href="/catalog" className="text-sm font-semibold text-emerald-400 hover:underline">View All &rarr;</a>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {FEATURED_PRODUCTS.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      </section>
    </div>
  );
}
"""
        fm.create_file("app/page.tsx", store_home_tsx, overwrite=True)

        # 9. app/catalog/page.tsx (Catalog with category filter & search)
        catalog_tsx = """import React from "react";
import ProductCard, { Product } from "@/components/ProductCard";

const ALL_PRODUCTS: Product[] = [
  { id: "1", name: "Ornàment Edge Node 64GB", category: "hardware", price: 899, rating: 4.9, description: "Local AI inference node with high bandwidth memory.", inStock: true },
  { id: "2", name: "Precision Split Keyboard", category: "gear", price: 249, rating: 4.8, description: "Columnar ergonomic developer keyboard.", inStock: true },
  { id: "3", name: "Thunderbolt 4 Dual Dock", category: "hardware", price: 189, rating: 4.7, description: "100W PD high throughput docking station.", inStock: true },
  { id: "4", name: "NVMe 4TB Gen5 SSD Enclosure", category: "hardware", price: 159, rating: 4.9, description: "Active aluminum cooling with 40Gbps interface.", inStock: true },
  { id: "5", name: "Desk Mat Ultra Minimal Black", category: "gear", price: 45, rating: 4.6, description: "High density micro-weave felt surface.", inStock: true }
];

export default function CatalogPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Hardware & Gear Catalog</h1>
        <p className="text-zinc-400 text-sm">Explore certified high-performance equipment for engineering workstations.</p>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between border-y border-zinc-800 py-4">
        <div className="flex space-x-2">
          <button className="px-3.5 py-1.5 rounded-lg bg-zinc-800 text-white text-xs font-semibold">All Items</button>
          <button className="px-3.5 py-1.5 rounded-lg border border-zinc-800 text-zinc-400 text-xs font-semibold hover:text-white">Hardware</button>
          <button className="px-3.5 py-1.5 rounded-lg border border-zinc-800 text-zinc-400 text-xs font-semibold hover:text-white">Gear</button>
        </div>
        <input
          type="search"
          aria-label="Filter catalog items"
          placeholder="Filter catalog..."
          className="px-4 py-2 rounded-lg bg-zinc-900 border border-zinc-800 text-sm text-white focus:outline-none focus:border-emerald-500 w-full sm:w-64"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {ALL_PRODUCTS.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
}
"""
        fm.create_file("app/catalog/page.tsx", catalog_tsx, overwrite=True)

        # 10. app/checkout/page.tsx (Checkout & Order Summary UI)
        checkout_tsx = """import React from "react";

export default function CheckoutPage() {
  return (
    <div className="py-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-8">Order Checkout</h1>
      <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
        <div className="md:col-span-7 space-y-6">
          <div className="p-6 rounded-xl border border-zinc-800 bg-zinc-900/60 space-y-4">
            <h2 className="text-lg font-bold text-white">Shipping Information</h2>
            <div className="grid grid-cols-2 gap-4">
              <input aria-label="First name" placeholder="First name" className="p-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-sm text-white" />
              <input aria-label="Last name" placeholder="Last name" className="p-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-sm text-white" />
            </div>
            <input aria-label="Shipping address" placeholder="Address" className="w-full p-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-sm text-white" />
            <div className="grid grid-cols-2 gap-4">
              <input aria-label="City" placeholder="City" className="p-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-sm text-white" />
              <input aria-label="Postal code" placeholder="Postal Code" className="p-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-sm text-white" />
            </div>
          </div>
        </div>

        <div className="md:col-span-5">
          <div className="p-6 rounded-xl border border-zinc-800 bg-zinc-900/80 space-y-4">
            <h2 className="text-lg font-bold text-white">Order Summary</h2>
            <div className="space-y-3 text-sm text-zinc-300 border-b border-zinc-800 pb-4">
              <div className="flex justify-between">
                <span>Ornàment Edge Node 64GB</span>
                <span className="font-mono text-white">$899.00</span>
              </div>
              <div className="flex justify-between">
                <span>Precision Split Keyboard</span>
                <span className="font-mono text-white">$249.00</span>
              </div>
            </div>
            <div className="flex justify-between font-bold text-lg text-white">
              <span>Total</span>
              <span className="text-emerald-400 font-mono">$1,148.00</span>
            </div>
            <button
              id="confirm-order-button"
              type="button"
              className="w-full py-3 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-black font-bold transition shadow-lg shadow-emerald-500/20"
            >
              Confirm & Pay
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
"""
        fm.create_file("app/checkout/page.tsx", checkout_tsx, overwrite=True)

        return {
            "status": "generated",
            "type": "e-commerce",
            "files_count": len(fm.list_files(exclude_build=True))
        }
