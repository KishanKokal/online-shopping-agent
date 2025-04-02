from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class SourcedFromEnum(str, Enum):
    myntra = "myntra"
    meesho = "meesho"
    ajio = "ajio"

class Product(BaseModel):
    product_name: str = Field(description="Name of the product")
    product_url: str = Field(
        description="URL to the product page (complete https link)"
    )
    product_image_url: str = Field(
        description="URL to the product image (complete https link)"
    )
    maximum_retail_price: float = Field(
        description="Maximum retail price of the productt"
    )
    selling_price: float = Field(description="Current selling price of the product")
    sourced_from: SourcedFromEnum = Field(
        description="E-commerce platform source of the product"
    )


class Products(BaseModel):
    products: List[Product]
