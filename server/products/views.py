from rest_framework.views import APIView
from langchain_openai import ChatOpenAI
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from .serializers import ProductSearchSerializer, ProductResponseSerializer, SourcedFromEnum
from browser_use import (
    Agent,
    Controller,
)
from dotenv import load_dotenv
import asyncio
from .models import Products
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Constants
WEBSITE_URLS: Dict[SourcedFromEnum, str] = {
    SourcedFromEnum.ajio: "https://www.ajio.com",
    SourcedFromEnum.meesho: "https://www.meesho.com",
    SourcedFromEnum.myntra: "https://www.myntra.com",
}
LLM_MODEL: str = "gpt-4o-mini"

# Load environment variables from .env file
load_dotenv()

class ProductSearchView(APIView):
    """
    API view for handling product search requests across multiple e-commerce websites.
    This view uses browser automation to search for products and return results in a standardized format.
    """
    def post(self, request: Request) -> Response:
        """
        Handle POST requests for product search.
        
        Args:
            request: HTTP request containing search query
            
        Returns:
            Response: JSON response containing search results or error message
        """
        try:
            # Validate incoming request data
            serializer: ProductSearchSerializer = ProductSearchSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Convert the query to a structured format and then to a search string
            search_query: str = serializer.to_search_string()
            
            # Initialize the language model and controller for browser automation
            llm: ChatOpenAI = ChatOpenAI(model=LLM_MODEL)
            controller: Controller = Controller(output_model=Products)
            
            # List to store all found products
            all_products: List[Dict[str, Any]] = []
            
            async def search_website(website: SourcedFromEnum) -> List[Dict[str, Any]]:
                """
                Search for products on a specific website using browser automation.
                
                Args:
                    website: Enum representing the website to search on
                    
                Returns:
                    list: List of products found on the website
                """
                try:
                    website_url: str = WEBSITE_URLS[website]
                    
                    # Create and configure the browser automation agent
                    agent: Agent = Agent(
                        task=f"""
INSTRUCTIONS FOR DATA COLLECTION:

When conducting a search on {website_url}, follow these steps to extract relevant product information:

1. Navigate to the website: Open {website_url} in a browser.
2. Perform a search: Locate the search box and enter the exact query: '{search_query}'. Press enter or click the search button.
3. Analyze the search results page: Focus on the first page and extract up to 10 most relevant products. Prioritize top-ranking results.
4. Extract the following details for each product:

   - Product Name: The name of the product as displayed on the website.
   - Product URL: The complete HTTPS link to the product's dedicated page.
   - Product Image URL: The full HTTPS link to the product's main image.
   - Maximum Retail Price (MRP): The original price before discounts (if available).
   - Discount Percentage: The percentage of discount applied (if any, otherwise 0).
   - Selling Price: The current price at which the product is being sold.
   - Sourced From: The name of the e-commerce platform where the product is listed.

5. If no products match the search criteria, **do not return anything**.


6. Ensure Accuracy & Formatting:
   - Extract only relevant products matching the search query.
   - Verify that URLs are complete and lead to the correct product pages.
   - Ensure numerical values (MRP, discount, selling price) are correctly formatted.
   - Return the data in valid JSON format based on the provided schema.
    {Products.model_json_schema()}
""",
                        llm=llm,
                        controller=controller,
                        use_vision=False,
                        initial_actions=[
                            {"open_tab": {"url": website_url}},
                        ],
                    )
                    
                    # Run the agent and get search results
                    history = await agent.run()
                    result: Optional[str] = history.final_result()
                    
                    # Parse and return results if available
                    if result:
                        parsed: Products = Products.model_validate_json(result)
                        for product in parsed.products:
                            if not product.maximum_retail_price:
                                product.maximum_retail_price = product.selling_price
                            product.discount_percentage = round(((product.maximum_retail_price - product.selling_price) / product.maximum_retail_price) * 100, 2)
                        parsed.products.sort(key=lambda p: p.selling_price)
                        return parsed.products
                    return []
                except Exception as e:
                    logger.error(f"Error searching {website}: {str(e)}")
                    return []
            
            async def search_all_websites() -> None:
                """
                Search for products across all specified websites concurrently.
                """
                websites_to_search = serializer.get_source_websites()
                
                tasks: List[asyncio.Task[List[Dict[str, Any]]]] = [
                    search_website(website) for website in websites_to_search
                ]
                
                results: List[List[Dict[str, Any]]] = await asyncio.gather(*tasks)
                for products in results:
                    all_products.extend(products)
            
            # Execute the concurrent search across all websites
            asyncio.run(search_all_websites())
            
            # Get the structured query to access max_price
            structured_query = serializer.to_structured_query()
            
            # Filter products based on max_price if it's set
            if structured_query.max_price is not None and structured_query.max_price > 0:
                all_products = [
                    product for product in all_products 
                    if product.selling_price <= structured_query.max_price
                ]
            
            # Serialize and return the results
            response_serializer: ProductResponseSerializer = ProductResponseSerializer(all_products, many=True)
            return Response(response_serializer.data)
            
        except Exception as e:
            logger.error(f"Unexpected error in product search: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred while processing your request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_website_url(self, website: SourcedFromEnum) -> str:
        """
        Get the base URL for a given e-commerce website.
        
        Args:
            website: Enum representing the website
            
        Returns:
            str: Base URL of the website
        """
        return WEBSITE_URLS.get(website, WEBSITE_URLS[SourcedFromEnum.myntra])