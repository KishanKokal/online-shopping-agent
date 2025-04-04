import { Button } from '@/components/ui/button';
import myntra_logo from '@/assets/myntra-logo.png';
import meesho_logo from '@/assets/meeho-logo.png';
import ajio_logo from '@/assets/ajio-logo.png';
import flipkart_logo from '@/assets/flipkart-logo.png';
import { ProductGridProps } from '@/pages/search';
import { Skeleton } from '@/components/ui/skeleton';

export default function ProductGrid({ products, searching }: ProductGridProps) {
  // Map the logo based on the source
  const getSourceLogo = (source: string) => {
    switch (source.toLowerCase()) {
      case 'myntra':
        return myntra_logo; // Replace with your actual logo path
      case 'meesho':
        return meesho_logo;
      case 'flipkart':
        return flipkart_logo;
      case 'ajio':
        return ajio_logo;
    }
  };

  // Format price to Indian Rupee format
  const formatPrice = (price: number) => {
    return `₹${price.toLocaleString('en-IN')}`;
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {searching
        ? Array.from({ length: 8 }).map((_, idx) => (
            <div
              key={idx}
              className="bg-[#1a1a1a] rounded-lg p-4 flex flex-col gap-4"
            >
              <Skeleton className="w-full aspect-square rounded-md bg-[#2b2b2b]" />
              <Skeleton className="h-4 w-3/4 bg-[#2b2b2b]" />
              <Skeleton className="h-4 w-1/2 bg-[#2b2b2b]" />
            </div>
          ))
        : products.map((product, index) => (
            <div
              key={index}
              className="bg-[#1a1a1a] rounded-lg overflow-hidden flex flex-col"
            >
              <a
                href={product.product_url}
                target="_blank"
                rel="noopener noreferrer"
                className="relative block"
              >
                {/* Image container with fixed aspect ratio but showing full image */}
                <div className="aspect-square flex items-center justify-center overflow-hidden bg-gray-800">
                  <img
                    src={
                      product.product_image_url || '/api/placeholder/400/400'
                    }
                    alt={product.product_name}
                    width={300}
                    height={300}
                    className="object-contain w-full h-full"
                  />
                </div>
                {product.discount_percentage > 0 && (
                  <div className="absolute top-2 left-2 bg-green-600 text-white px-2 py-1 text-sm font-medium rounded">
                    {product.discount_percentage}% OFF
                  </div>
                )}
              </a>
              <div className="p-4 flex flex-col gap-4 flex-grow">
                <div className="flex justify-between items-center">
                  <div className="flex flex-col gap-1 w-5/6">
                    <h3 className="text-lg font-medium text-gray-200 line-clamp-1">
                      {product.product_name}
                    </h3>
                    <div className="flex items-end gap-2">
                      <span className="text-3xl font-bold">
                        {formatPrice(product.selling_price)}
                      </span>
                      {product.discount_percentage > 0 && (
                        <span className="text-gray-400 line-through text-lg">
                          {formatPrice(product.maximum_retail_price)}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="w-1/6 flex flex-col">
                    <img
                      src={getSourceLogo(product.sourced_from)}
                      alt={`${product.sourced_from} logo`}
                      className="rounded-md w-full h-full"
                    />
                  </div>
                </div>
                <a
                  href={product.product_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full"
                >
                  <Button className="w-full bg-[#1a1a1a] hover:bg-[#333] border border-[#333] text-white rounded-md py-2 mt-auto">
                    Buy
                  </Button>
                </a>
              </div>
            </div>
          ))}
    </div>
  );
}
