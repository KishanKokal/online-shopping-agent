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
                    'content': "You are a helpful assistant that helps standardize a user's query into a structured format. Extract relevant information about item name, colors, sizes, price range, material, and gender from the query."
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
            return StructuredSearchQuery(item_name=self.validated_data['query'])
    
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
    
    def get_source_websites(self) -> list[SourcedFromEnum]:
        """
        Get the list of websites to source products from.
        If source_from is None or empty, return all available websites.
        Otherwise, return the list of websites specified in the query.
        
        Returns:
            list[SourcedFromEnum]: List of websites to source products from
        """
        structured_query = self.to_structured_query()
        
        # If source_from is None or empty, return all available websites
        if not structured_query.source_from:
            return list(SourcedFromEnum)
        
        # Return the list of websites specified in the query
        return structured_query.source_from

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