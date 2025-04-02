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
            request: HTTP request containing search query and target websites
            
        Returns:
            Response: JSON response containing search results or error message
        """
        try:
            # Validate incoming request data
            serializer: ProductSearchSerializer = ProductSearchSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract validated data from request
            query: str = serializer.validated_data['query']
            websites: List[str] = serializer.validated_data['websites']
            
            # Initialize the language model and controller for browser automation
            llm: ChatOpenAI = ChatOpenAI(model=LLM_MODEL)
            controller: Controller = Controller(output_model=Products)
            
            # List to store all found products
            all_products: List[Dict[str, Any]] = []
            
            async def search_website(website: str) -> List[Dict[str, Any]]:
                """
                Search for products on a specific website using browser automation.
                
                Args:
                    website: Name of the website to search on
                    
                Returns:
                    list: List of products found on the website
                """
                try:
                    # Convert website name to enum and get corresponding URL
                    website_enum: SourcedFromEnum = SourcedFromEnum(website)
                    website_url: str = self.get_website_url(website_enum)
                    
                    # Create and configure the browser automation agent
                    agent: Agent = Agent(
                        task=f"""Go to {website_url} exactly enter the following query '{query}' in the search box and press enter and, return the top 10 results in JSON format:
                        - extract and return the information in a **valid JSON** following the schema:
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
                        return parsed.products
                    return []
                except Exception as e:
                    logger.error(f"Error searching {website}: {str(e)}")
                    return []
            
            async def search_all_websites() -> None:
                """
                Search for products across all specified websites concurrently.
                """
                tasks: List[asyncio.Task[List[Dict[str, Any]]]] = [search_website(website) for website in websites]
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