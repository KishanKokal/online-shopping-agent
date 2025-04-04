import { Search } from 'lucide-react';
import ProductGrid from '@/components/product-grid';
import logo from '@/assets/fynd-logo.png';
import { useState, useRef } from 'react';
import axios from 'axios';

export interface Product {
  product_name: string;
  product_url: string;
  product_image_url: string;
  maximum_retail_price: number;
  discount_percentage: number;
  selling_price: number;
  sourced_from: string;
}

export interface ProductGridProps {
  products: Product[];
  searching: boolean;
}

interface SearchRequestDto {
  query: string;
}

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const [products, setProducts] = useState<Product[]>([]);
  const [searching, setSearching] = useState(false);

  const inputRef = useRef<HTMLInputElement>(null);

  const fetchProdutcs = async () => {
    const searchRequest: SearchRequestDto = {
      query: searchQuery,
    };
    inputRef.current?.blur();
    setSearching(true);
    try {
      const response = await axios.post<Product[]>(
        'http://localhost:8000/api/search/',
        searchRequest
      );
      setProducts(response.data);
    } catch (e) {
      console.log((e as Error).message);
    } finally {
      setSearching(false);
    }
  };

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
            ref={inputRef}
            placeholder="Search..."
            value={searchQuery}
            onChange={e => {
              e.preventDefault(); // Prevent form submission (if needed)
              setSearchQuery(e.target.value);
            }}
            onKeyDown={e => {
              if (e.key === 'Enter') {
                fetchProdutcs();
                e.preventDefault(); // Prevent form submission (if needed)
              }
            }}
            className="w-full bg-[#1e1e1e] border border-[#333] rounded-full py-3 px-6 text-white focus:outline-none"
          />
          <button
            className="absolute right-4 top-1/2 -translate-y-1/2"
            onClick={fetchProdutcs}
          >
            <Search className="w-6 h-6 text-white" />
          </button>
        </div>

        {/* Product Grid */}
        <ProductGrid products={products} searching={searching} />
      </div>
    </main>
  );
}
