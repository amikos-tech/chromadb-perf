import uuid
from typing import Any, Optional, List, Dict

from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse
import orjson
from pydantic import BaseModel

from chromadb import DEFAULT_DATABASE, DEFAULT_TENANT
from chromadb.server.fastapi import CreateCollection, AddEmbedding
from chromadb.types import Database, Collection


class ORJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


app = FastAPI(default_response_class=ORJSONResponse)


@app.get("/api/v1/tenants/{tenant}")
def get_tenant(tenant: str) -> Dict[str, str]:
    return {"name": tenant}


@app.get("/api/v1/databases/{db}")
def get_database(db: str, tenant: str) -> Database:
    return Database(id=uuid.uuid4(), name=db, tenant=tenant)


@app.post("/api/v1/collections")
def create_collection(collection: CreateCollection,
                      tenant: str = DEFAULT_TENANT,
                      database: str = DEFAULT_DATABASE, ) -> Collection:
    return Collection(
        id=uuid.uuid4(),
        name=collection.name,
        topic="dqwwqeqw",
        metadata=collection.metadata,
        dimension=None,
        tenant=tenant,
        database=database,
    )


@app.get("/api/v1/pre-flight-checks")
def pre_flight_checks() -> Dict[str, Any]:
    return {"max_batch_size": 100000}


@app.post("/api/v1/collections/{collection_id}/add")
async def add(request: Request) -> None:
    # raw_body = await request.body()
    # cid = request.path_params.get("collection_id")
    # parsed_body = orjson.loads(raw_body)
    # item = AddEmbedding.model_validate(parsed_body)
    # print(cid, len(item.ids))
    return None


@app.get("/api/v1/version")
def version() -> str:
    return "0.1.0"
