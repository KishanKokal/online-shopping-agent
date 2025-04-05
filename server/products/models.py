from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class SizeEnum(str, Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "2XL"
    XXXL = "3XL"
    XXXXL = "4XL"

class GenderEnum(str, Enum):
    Men = "Men"
    Women = "Women"

class SourcedFromEnum(str, Enum):
    myntra = "myntra"
    meesho = "meesho"
    ajio = "ajio"
    flipkart = "flipkart"

class StructuredSearchQuery(BaseModel):
    item_name: str = Field(
        description="The specific product being searched for (e.g., jeans, t-shirt, sneakers)"
    )
    item_colors: Optional[List[str]] = Field(
        default=None,
        description="List of colors mentioned in the query (e.g., red, blue, black)"
    )
    item_sizes: Optional[List[SizeEnum]] = Field(
        default=None,
        description="List of size specifications mentioned in the query"
    )
    min_price: Optional[float] = Field(
        default=None,
        description="Minimum price constraint specified in the query"
    )
    max_price: Optional[float] = Field(
        default=None,
        description="Maximum price constraint specified in the query"
    )
    material: Optional[str] = Field(
        default=None,
        description="Fabric or material preference mentioned in the query (e.g., cotton, leather)"
    )
    gender: Optional[GenderEnum] = Field(
        default=None,
        description="Target gender for the product (men, women, kids, or unisex)"
    )
    source_from: Optional[List[SourcedFromEnum]] = Field(
        default=None,
        description="List of supported e-commerce platforms mentioned in the query"
    )
    unsupported_platforms: Optional[List[str]] = Field(
        default=None,
        description="List of e-commerce platforms mentioned that aren't in our supported list"
    )
    has_only_unsupported_platforms: bool = Field(
        description="True if query mentions platforms but none are supported, False otherwise"
    )

class Product(BaseModel):
    product_name: str = Field(description="Name of the product. It should capture the most relevant product description from the query, including any key modifiers (e.g., 'oversized t-shirts', 'running shoes', 'slim fit jeans')")
    product_url: str = Field(
        description="URL to the product page (complete https link)"
    )
    product_image_url: str = Field(
        description="URL to the product image (complete https link)"
    )
    maximum_retail_price: float | None = Field(
        description="Maximum retail price of the product"
    )
    discount_percentage: int | None = 0
    selling_price: float = Field(description="Current selling price of the product")
    sourced_from: SourcedFromEnum = Field(
        description="E-commerce platform source of the product"
    )


class Products(BaseModel):
    products: List[Product]

# Define a validation model for query safety checks
class QueryValidationResult(BaseModel):
    is_safe: bool = Field(description="Whether the query is a legitimate product search")
    reason: Optional[str] = Field(None, description="Reason why query was rejected if unsafe")
