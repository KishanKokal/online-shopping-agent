from rest_framework import serializers
from .models import SourcedFromEnum, StructuredSearchQuery
from typing import Tuple, List, Optional
from openai import OpenAI

class ProductSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, help_text="Natural language search query for products")
    
    def to_structured_query(self) -> StructuredSearchQuery:
        """
        Convert the natural language query to a structured search query using GPT-4.
        First validates the query for safety, then processes it if safe.
        
        Returns:
            StructuredSearchQuery: The structured query object
        """
        client = OpenAI()
        query = self.validated_data['query']
        
        try:
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {
                        'role': 'system',
                        'content': f"""You are a helpful assistant that standardizes user queries into a structured format matching our StructuredSearchQuery model.

                For e-commerce platforms analysis:
                - source_from: List of ONLY the supported platforms mentioned in the query
                - unsupported_platforms: List of platforms mentioned that aren't in our supported list
                - has_only_unsupported_platforms: Boolean, must be true if query mentions platforms but none are supported, false otherwise

                The list of supported platforms (SourcedFromEnum) is:
                {[platform.value for platform in SourcedFromEnum]}

                Return a JSON object strictly following the StructuredSearchQuery model structure. Do not include additional fields not in the model. Set fields to null when no relevant information is found, except for has_only_unsupported_platforms which must be a boolean.

                IMPORTANT INSTRUCTIONS:
                - You can always return null for values that are not explicitly mentioned by the user like if the user doesn't mention the sizes in the query, return a null value
                - The **item_name** field should capture the most relevant product description from the query, including any key modifiers (e.g., "oversized t-shirts", "running shoes", "slim fit jeans"). It should reflect what the user is specifically looking for and not be overly generalized.

                
                EXAMPLE OUTPUTS:
                Query: "find men's black jeans under 2000 on flipkart"
                {{
                    "item_name": "jeans",
                    "item_colors": ["black"],
                    "item_sizes": null,
                    "min_price": null,
                    "max_price": 2000,
                    "material": null,
                    "gender": "men",
                    "source_from": ["flipkart"],
                    "unsupported_platforms": null,
                    "has_only_unsupported_platforms": false
                }}

                Query: "white cotton t-shirts on amazon between 500 and 1500"
                {{
                    "item_name": "t-shirts",
                    "item_colors": ["white"],
                    "item_sizes": null,
                    "min_price": 500,
                    "max_price": 1500,
                    "material": "cotton",
                    "gender": null,
                    "source_from": [],
                    "unsupported_platforms": ["amazon"],
                    "has_only_unsupported_platforms": true
                }}

                Query: "search for men oversized t-shirts under 1000rs on myntra"
                {{
                    "item_name": "oversized t-shirts",
                    "item_colors": null,
                    "item_sizes": null,
                    "min_price": null,
                    "max_price": 1000,
                    "material": null,
                    "gender": "men",
                    "source_from": ["myntra"],
                    "unsupported_platforms": null,
                    "has_only_unsupported_platforms": false
                }}

                """
                    },
                    {
                        'role': 'user',
                        'content': query
                    }
                ],
                response_format=StructuredSearchQuery
            )
            print(completion.choices[0].message.parsed)
            return completion.choices[0].message.parsed
            
        except Exception as e:
            # If parsing fails, create a basic query with just the item name
            print("Error converting to structured query")
            return StructuredSearchQuery(
                item_name=query,
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
    
    def get_source_websites(self) -> Tuple[List[SourcedFromEnum], Optional[str]]:
        """
        Get the list of websites to source products from and check for unsupported platforms.
        If source_from is None or empty, return all available websites.
        Otherwise, return the list of supported websites specified in the query and a message about unsupported platforms.
        
        Returns:
            tuple[list[SourcedFromEnum], str | None]: List of supported websites to source products from and a message about unsupported platforms
        """
        structured_query = self.to_structured_query()
        
        # If the query was invalid (rejected by validation), return empty list
        if structured_query.item_name == "invalid_query":
            return [], "Invalid query. Please search for products only."
        
        # If source_from is None or empty and no unsupported platforms, return all available websites
        if not structured_query.source_from and not structured_query.unsupported_platforms:
            return list(SourcedFromEnum), None
        
        # If there are unsupported platforms, create a message
        message = None
        if structured_query.unsupported_platforms:
            unsupported_list = ", ".join(structured_query.unsupported_platforms)
            message = f"We currently don't support the following platforms: {unsupported_list}. We're working on adding support for more platforms."
        
        # If no supported platforms were requested, return empty list with message
        if structured_query.has_only_unsupported_platforms or not structured_query.source_from:
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