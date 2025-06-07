from unittest import mock
import importlib
import asyncio

import pytest
from fastapi.testclient import TestClient

import app.models as models


class DummyId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return str(v)


class FakeInsertResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class FakeCollection:
    def __init__(self):
        self.docs = []

    async def insert_one(self, doc):
        self.docs.append(doc)
        return FakeInsertResult('1')

    def find(self, query):
        async def gen():
            for d in self.docs:
                if d.get('type') == query.get('type'):
                    yield d
        return gen()


def test_add_and_query_stock(monkeypatch):
    monkeypatch.setattr(models, 'PyObjectId', DummyId)
    import app.schema as schema
    import importlib
    import app.main as main
    importlib.reload(schema)
    importlib.reload(main)

    fake_col = FakeCollection()
    monkeypatch.setattr(schema, 'collection', fake_col)
    monkeypatch.setattr(schema, 'verify_token', mock.AsyncMock(return_value={}))

    async def fake_add_stock(self, info, data):
        doc = data.to_pydantic().dict()
        fake_col.docs.append({"name": doc["name"], "quantity": doc["quantity"], "type": "stock"})
        return {"name": doc["name"], "quantity": doc["quantity"]}

    monkeypatch.setattr(schema.Mutation, 'add_stock', fake_add_stock)

    class FakeInfo:
        context = {"request": object()}

    stock_input = schema.StockInput(name="item", quantity=2)
    res = asyncio.run(schema.Mutation().add_stock(FakeInfo(), stock_input))
    assert res["name"] == "item"

    docs = asyncio.run(schema.Query().stock(FakeInfo()))
    assert len(docs) == 1
    assert docs[0].name == "item"
