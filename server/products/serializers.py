from rest_framework import serializers
from .models import SourcedFromEnum

# Serializer for handling product search requests
# Used to validate and process incoming search queries from clients
class ProductSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, help_text="Search query for products")
    websites = serializers.ListField(
        child=serializers.ChoiceField(choices=[(x.value, x.value) for x in SourcedFromEnum]),
        required=True,
        help_text="List of websites to search from (myntra, meesho, ajio)"
    )

# Serializer for formatting product search results
# Used to structure and validate product data before sending to clients
class ProductResponseSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    product_url = serializers.URLField()
    product_image_url = serializers.URLField()
    maximum_retail_price = serializers.FloatField()
    selling_price = serializers.FloatField()
    sourced_from = serializers.ChoiceField(choices=[(x.value, x.value) for x in SourcedFromEnum])