import { Search } from 'lucide-react';
import ProductGrid from '@/components/product-grid';
import logo from '@/assets/fynd-logo.png';

export default function Home() {
  return (
    <main className="min-h-screen bg-[#121212] text-white p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header with Logo */}
        <header className="flex justify-center items-center mb-10 mt-6">
          <img
            src={logo}
            alt="Logo"
            className="h-20 w-auto border border-white rounded-full"
          />
        </header>

        {/* Search Bar */}
        <div className="relative mb-8">
          <input
            type="text"
            placeholder="Search..."
            className="w-full bg-[#1e1e1e] border border-[#333] rounded-full py-3 px-6 text-white focus:outline-none"
          />
          <button className="absolute right-4 top-1/2 -translate-y-1/2">
            <Search className="w-6 h-6 text-white" />
          </button>
        </div>

        {/* Product Grid */}
        <ProductGrid />
      </div>
    </main>
  );
}
