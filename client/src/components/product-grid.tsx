import { Button } from '@/components/ui/button';
import myntra_logo from '@/assets/myntra-logo.png';
import meesho_logo from '@/assets/meeho-logo.png';

export default function ProductGrid() {
  // This is the actual data from the server
  const products = [
    {
      product_name:
        'THIRD QUADRANT Men Abstract Printed Round Neck Cotton Oversized T-shirt',
      product_url:
        'https://www.myntra.com/tshirts/third+quadrant/third-quadrant-men-abstract-printed-round-neck-cotton-oversized-t-shirt/30895216/buy',
      product_image_url:
        'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/2024/SEPTEMBER/7/HJoG9Tc4_3cc4f03b6b534eeab471d98d17f15e90.jpg',
      maximum_retail_price: 1699,
      discount_percentage: 60,
      selling_price: 679,
      sourced_from: 'myntra',
    },
    {
      product_name:
        'Snitch Men Graphic Printed Round Neck Cotton Oversized T-shirt',
      product_url:
        'https://www.myntra.com/tshirts/snitch/snitch-men-graphic-printed-round-neck-cotton-oversized-t-shirt/32416010/buy',
      product_image_url:
        'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/2025/JANUARY/22/HupLjC3I_281bedc94e22423facf181c9e484ba4c.jpg',
      maximum_retail_price: 999,
      discount_percentage: 0,
      selling_price: 999,
      sourced_from: 'myntra',
    },
    {
      product_name: 'ONEWAY Unisex Solid Oversized Cotton T-shirt',
      product_url:
        'https://www.myntra.com/tshirts/oneway/oneway-unisex-solid-oversized-cotton-t-shirt/33132876/buy',
      product_image_url:
        'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/2025/MARCH/11/X0KRHZ7I_e12876f3fc1a4472aad735eea49d94a4.jpg',
      maximum_retail_price: 799,
      discount_percentage: 30,
      selling_price: 559,
      sourced_from: 'myntra',
    },
    {
      product_name: 'Crazymonk Unisex Anime Printed Oversized T-shirt',
      product_url:
        'https://www.myntra.com/tshirts/crazymonk/crazymonk-unisex-anime-printed-oversized-t-shirt/24357700/buy',
      product_image_url:
        'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/24357700/2023/8/5/07a5b0c0-58d1-4939-aeb5-5b8bd3cf39961691231422609CrazymonkUnisexLavenderPrintedPocketsT-shirt1.jpg',
      maximum_retail_price: 1499,
      discount_percentage: 53,
      selling_price: 704,
      sourced_from: 'myntra',
    },
    {
      product_name:
        'THIRD QUADRANT Men Typography Printed Round Neck Cotton Oversized T-shirt',
      product_url:
        'https://www.myntra.com/tshirts/third+quadrant/third-quadrant-men-typography-printed-round-neck-cotton-oversized-t-shirt/30940591/buy',
      product_image_url:
        'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/2024/SEPTEMBER/11/4iN6zCmy_478960174fe24706a2f154ec9bb590df.jpg',
      maximum_retail_price: 1699,
      discount_percentage: 60,
      selling_price: 679,
      sourced_from: 'myntra',
    },
    {
      product_name:
        'Gavin Paris Graphic Printed Drop Shoulder Sleeves Oversized T-shirt',
      product_url:
        'https://www.myntra.com/tshirts/gavin+paris/gavin-paris-graphic-printed-drop-shoulder-sleeves-oversized-t-shirt/23425964/buy',
      product_image_url:
        'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/23425964/2023/5/26/5518c284-573a-430d-8099-6bf7c750d8df1685104648060GavinParisUnisexWhiteAppliqueLooseT-shirt1.jpg',
      maximum_retail_price: 1599,
      discount_percentage: 65,
      selling_price: 559,
      sourced_from: 'myntra',
    },
    {
      product_name: 'Bewakoof Oversized Cotton T-shirt',
      product_url:
        'https://www.myntra.com/tshirts/bewakoof/bewakoof-peanuts-graphic-printed-drop-shoulder-sleeves-oversized-cotton-t-shirt/28037952/buy',
      product_image_url:
        'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/28037952/2023/5/20/a90b7d72-37bc-4ff1-bb10-d2267a97ce11.jpg',
      maximum_retail_price: 1299,
      discount_percentage: 51,
      selling_price: 636,
      sourced_from: 'myntra',
    },
    {
      product_name: 'Snitch Men Solid Round Neck Oversized Cotton T-shirt',
      product_url:
        'https://www.myntra.com/tshirts/snitch/snitch-men-solid-round-neck-oversized-cotton-t-shirt/32075044/buy',
      product_image_url:
        'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/32075044/2024/12/25/99c3c3b6-32cd-4823-9c73-f331e944945c1735123595905SnitchMenDrop-ShoulderSleevesSlimFitT-shirt1.jpg',
      maximum_retail_price: 2398,
      discount_percentage: 66,
      selling_price: 799,
      sourced_from: 'meesho',
    },
    {
      product_name:
        'Crazymonk Unisex Zenistu Demon Slayer Anime Printed Cotton Oversized T-shirt',
      product_url:
        'https://www.myntra.com/tshirts/crazymonk/crazymonk-unisex-zenistu-demon-slayer-anime-printed-cotton-oversized-t-shirt/26684200/buy',
      product_image_url:
        'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/26684200/2023/12/27/69a6b936-9c20-419f-845a-ae118b607a101703673911746CrazymonkUnisexYellowPrintedT-shirt1.jpg',
      maximum_retail_price: 1499,
      discount_percentage: 53,
      selling_price: 704,
      sourced_from: 'myntra',
    },
    {
      product_name: 'Maniac Striped Round Neck T-shirt',
      product_url:
        'https://www.myntra.com/tshirts/maniac/maniac-striped-round-neck-t-shirt/28727814/buy',
      product_image_url:
        'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/28727814/2024/4/6/c19682d1-9d4c-4d38-9451-45331bab81851712384125011ManiacMenStripedV-NeckDrop-ShoulderSleevesPocketsT-shirt1.jpg',
      maximum_retail_price: 1569,
      discount_percentage: 69,
      selling_price: 486,
      sourced_from: 'myntra',
    },
  ];

  // Map the logo based on the source
  const getSourceLogo = (source: string) => {
    switch (source.toLowerCase()) {
      case 'myntra':
        return myntra_logo; // Replace with your actual logo path
      case 'meesho':
        return meesho_logo;
      default:
        return '/placeholder.svg';
    }
  };

  // Format price to Indian Rupee format
  const formatPrice = (price: number) => {
    return `₹${price.toLocaleString('en-IN')}`;
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {products.map((product, index) => (
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
                src={product.product_image_url || '/api/placeholder/400/400'}
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
