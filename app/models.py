from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        return ObjectId(str(v))

class StockItem(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    quantity: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Order(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    items: List[str]
    total: float

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Quote(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    items: List[str]
    total: float
    pdf_path: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Invoice(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    items: List[str]
    total: float
    pdf_path: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
