import os
import time
import uuid

from locust import task, User, events, between

import chromadb


class UserBehavior(User):
    wait_time = between(0.1, 0.2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch_size = int(os.getenv('BATCH_SIZE', '100'))
        self.dimensions = int(os.getenv('DIMENSIONS', '1536'))

    def on_start(self):
        try:
            self.client = chromadb.HttpClient()
            self.collection = self.client.create_collection("test_collection")
        except Exception as e:
            print(e)

    @staticmethod
    def get_batch(batch_size: int, dimensions: int):
        return zip(*[(f"{uuid.uuid4()}", f"document {i}", [0.1] * dimensions) for i in range(batch_size)])

    @task
    def my_task(self):
        ids, documents, embeddings = self.get_batch(self.batch_size, self.dimensions)
        start_time = time.perf_counter()
        req_metadata = {
            "request_type": "chroma",
            "name": "my_task",
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
