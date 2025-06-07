from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter

from .schema import schema
from .voice import router as voice_router

app = FastAPI(title="OperAI ERP")

gql_router = GraphQLRouter(schema)

@app.middleware("http")
async def add_request_to_context(request: Request, call_next):
    request.state.context = {"request": request}
    response = await call_next(request)
    return response

app.include_router(gql_router, prefix="/graphql")
app.include_router(voice_router)
