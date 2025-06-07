import strawberry
from typing import List, Annotated

from .models import StockItem, Order, Quote, Invoice
from .database import collection
from .utils import generate_pdf
from .auth import verify_token

@strawberry.experimental.pydantic.input(model=StockItem, fields=["name", "quantity"])
class StockInput:
    pass

@strawberry.experimental.pydantic.type(model=StockItem, fields=["name", "quantity"])
class StockType:
    pass

@strawberry.type
class Query:
    @strawberry.field
    async def stock(self, info) -> List[StockType]:
        docs = collection.find({"type": "stock"})
        return [StockItem(**d) async for d in docs]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_stock(
        self,
        info,
        data: StockInput,
    ) -> StockType:
        await verify_token(info.context["request"])
        doc = data.to_pydantic().dict()
        doc["type"] = "stock"
        res = await collection.insert_one(doc)
        doc["_id"] = res.inserted_id
        return StockItem(**doc)

schema = strawberry.Schema(Query, Mutation)
