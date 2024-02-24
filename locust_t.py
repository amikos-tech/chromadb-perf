import os
import random
import time
import uuid

from chromadb import Settings
from locust import task, User, events, between, tag

import chromadb


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--batch-size", type=int, default=int(os.getenv('BATCH_SIZE', '100')), help="Batch Size")
    # parser.add_argument("--env", choices=["dev", "staging", "prod"], default="dev", help="Environment")
    parser.add_argument("--dimensions", type=int, default=int(os.getenv('DIMENSIONS', '1536')),
                        help="The number of dimensions for the embeddings")
    parser.add_argument("--collection", type=str, default="my_collection",
                        help="The name of the collection to use for the test")
    parser.add_argument("--chroma-host", type=str, default="localhost",
                        help="Chroma host")
    parser.add_argument("--port", type=int, default=8000,
                        help="Chroma port")


class UserBehavior(User):
    wait_time = between(0.01, 0.02)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch_size = self.environment.parsed_options.batch_size
        self.dimensions = self.environment.parsed_options.dimensions
        try:
            self.client = chromadb.HttpClient(host=self.environment.parsed_options.chroma_host,
                                              port=self.environment.parsed_options.port,
                                              settings=Settings(anonymized_telemetry=False))
            self.collection = self.client.get_collection(self.environment.parsed_options.collection)
        except Exception as e:
            print(e)
            raise e

    def on_start(self):
        pass

    @staticmethod
    def get_batch(batch_size: int, dimensions: int):
        return zip(*[(f"{uuid.uuid4()}", f"document {i}", [0.1] * dimensions) for i in range(batch_size)])

    @tag("add", "batch", "random")
    @task
    def batch_add(self):
        ids, documents, embeddings = self.get_batch(self.batch_size, self.dimensions)
        start_time = time.perf_counter()
        req_metadata = {
            "request_type": "chroma",
            "name": "add",
            "start_time": start_time,
            "response_length": 0,
            "response": None,
            "context": {},  # see HttpUser if you actually want to implement contexts
            "exception": None,
        }
        try:
            self.collection.add(ids=list(ids), documents=list(documents), embeddings=list(embeddings))
            total_time = int((time.perf_counter() - start_time) * 1000)
            req_metadata["response_time"] = total_time
            events.request.fire(**req_metadata)
        except Exception as e:
            total_time = int((time.perf_counter() - start_time) * 1000)
            req_metadata["response_time"] = total_time
            req_metadata["exception"] = e
            events.request.fire(**req_metadata)

    @tag("query", "dataset")
    @task
    def query_chroma(self):
        count = self.collection.count()
        random_id = random.randint(0, count)
        res = self.collection.get(offset=random_id, limit=1, include=["embeddings"])
        start_time = time.perf_counter()
        req_metadata = {
            "request_type": "chroma",
            "name": "query",
            "start_time": start_time,
            "response_length": 0,
            "response": None,
            "context": {},  # see HttpUser if you actually want to implement contexts
            "exception": None,
        }
        try:
            self.collection.query(query_embeddings=[res['embeddings'][0]],
                                  where={"$and": [{"rand": {"$gte": 501}}, {"rand": {"$lte": 502}}]})
            total_time = int((time.perf_counter() - start_time) * 1000)
            req_metadata["response_time"] = total_time
            events.request.fire(**req_metadata)
        except Exception as e:
            total_time = int((time.perf_counter() - start_time) * 1000)
            req_metadata["response_time"] = total_time
            req_metadata["exception"] = e
            events.request.fire(**req_metadata)
