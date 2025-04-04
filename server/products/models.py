from pydantic import BaseModel, Field
from typing import List
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
    item_name: str
    item_colors: List[str] | None = None
    item_sizes: List[SizeEnum] | None = None
    min_price: int | float | None = None
    max_price: int | float | None = None
    material: str | None = None
    gender: GenderEnum | None = None
    source_from: List[SourcedFromEnum] | None = None
    unsupported_platforms: List[str] | None = None
    has_only_unsupported_platforms: bool

class Product(BaseModel):
    product_name: str = Field(description="Name of the product")
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
