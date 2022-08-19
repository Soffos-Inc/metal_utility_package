from ._base import ServiceRequestSession
from typing import List


class TransformerService(ServiceRequestSession):
    name = "soffos-service-model-transformers"

    def classify_query(self, query: str):
        
        json = {"query": query}

        return self.request(json=json, path="classify-query")

    def encode(self, texts: List[str], task: str = None):

        json = {"texts": texts}
        if task:
            json["task"] = task
            
        return self.request(json=json, path="sentence-bert/encode")
