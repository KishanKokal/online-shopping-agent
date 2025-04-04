from rest_framework import serializers
from .models import SourcedFromEnum, StructuredSearchQuery
from openai import OpenAI
import json

# Serializer for handling product search requests
# Used to validate and process incoming search queries from clients
class ProductSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, help_text="Natural language search query for products")
    
    def to_structured_query(self) -> StructuredSearchQuery:
        """
        Convert the natural language query to a structured search query using GPT-4.
        
        Returns:
            StructuredSearchQuery: The structured query object
        """
        client = OpenAI()
        
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    'role': 'system',
                    'content': """You are a helpful assistant that helps standardize a user's query into a structured format. 
                    Extract relevant information about:
                    - item name, colors, sizes, price range, material, and gender from the query
                    - e-commerce platforms mentioned in the query
                    - identify if the query mentions any platforms not in our supported list (myntra, meesho, ajio, flipkart)
                    
                    For platforms, you should:
                    1. Identify all platforms mentioned in the query
                    2. Separate them into supported (myntra, meesho, ajio, flipkart) and unsupported platforms
                    3. Set has_only_unsupported_platforms to true if the query only mentions unsupported platforms
                    4. Set source_from to the list of supported platforms mentioned
                    5. Set unsupported_platforms to the list of unsupported platforms mentioned
                    
                    Example response for "search for tshirts on amazon and flipkart":
                    {
                        "item_name": "tshirts",
                        "source_from": [],
                        "unsupported_platforms": ["amazon"],
                        "has_only_unsupported_platforms": true
                    }
                    
                    Example response for "search for tshirts on myntra and amazon":
                    {
                        "item_name": "tshirts",
                        "source_from": ["myntra"],
                        "unsupported_platforms": ["amazon"],
                        "has_only_unsupported_platforms": false
                    }"""
                },
                {
                    'role': 'user',
                    'content': self.validated_data['query']
                }
            ],
            response_format=StructuredSearchQuery
        )
        
        # Parse the response into a StructuredSearchQuery
        try:
            parsed_data = json.loads(completion.choices[0].message.content)
            return StructuredSearchQuery(**parsed_data)
        except Exception as e:
            # If parsing fails, create a basic query with just the item name
            return StructuredSearchQuery(
                item_name=self.validated_data['query'],
                has_only_unsupported_platforms=False
            )
    
    def to_search_string(self) -> str:
        """
        Convert the structured query into a standardized search string.
        
        Returns:
            str: The standardized search string
        """
        structured_query = self.to_structured_query()
        parts = []
        
        if structured_query.gender:
            parts.append(structured_query.gender)
        
        if structured_query.material:
            parts.append(structured_query.material)
            
        if structured_query.item_colors:
            parts.extend(structured_query.item_colors)
            
        parts.append(structured_query.item_name)
        
        if structured_query.max_price:
            parts.append(f"under {structured_query.max_price}")
            
        if structured_query.item_sizes:
            parts.append(f"size {' '.join(structured_query.item_sizes)}")
            
        return " ".join(parts)
    
    def get_source_websites(self) -> tuple[list[SourcedFromEnum], str | None]:
        """
        Get the list of websites to source products from and check for unsupported platforms.
        If source_from is None or empty, return all available websites.
        Otherwise, return the list of supported websites specified in the query and a message about unsupported platforms.
        
        Returns:
            tuple[list[SourcedFromEnum], str | None]: List of supported websites to source products from and a message about unsupported platforms
        """
        structured_query = self.to_structured_query()
        
        # If source_from is None or empty and no unsupported platforms, return all available websites
        if not structured_query.source_from and not structured_query.unsupported_platforms:
            return list(SourcedFromEnum), None
        
        # If there are unsupported platforms, create a message
        message = None
        if structured_query.unsupported_platforms:
            unsupported_list = ", ".join(structured_query.unsupported_platforms)
            message = f"We currently don't support the following platforms: {unsupported_list}. We're working on adding support for these platforms."
        
        # If no supported platforms were requested, return empty list with message
        if not structured_query.source_from:
            return [], message
        
        # Return supported platforms and message about unsupported ones
        return list(structured_query.source_from), message

# Serializer for formatting product search results
# Used to structure and validate product data before sending to clients
class ProductResponseSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    product_url = serializers.URLField()
    product_image_url = serializers.URLField()
    maximum_retail_price = serializers.FloatField()
    discount_percentage = serializers.IntegerField()
    selling_price = serializers.FloatField()
    sourced_from = serializers.ChoiceField(choices=[(x.value, x.value) for x in SourcedFromEnum])