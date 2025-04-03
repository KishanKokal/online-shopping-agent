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
                        task=f"""Visit {website_url} and perform a search for '{search_query}'. 
    
                        INSTRUCTIONS:
                        1. Navigate to the exact URL: {website_url}
                        2. Locate the search box on the page
                        3. Enter the exact query: '{search_query}' (without quotes)
                        4. Press enter or click the search button
                        5. Analyze the search results page
                        6. Extract up to 10 most relevant products/items from the search results
                        7. Focus on the products displayed on the first page
                        
                        When extracting data:
                        - Capture up to 10 most relevant products that best match the search criteria
                        - Prioritize products that appear at the top of the search results
                        - Ensure the data is formatted according to the provided schema
                        - Return the data as valid JSON following this schema:
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