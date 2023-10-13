import ray
from sentence_transformers import SentenceTransformer
import bson
import requests

ray.init()

@ray.remote
class EmbeddingService:
    def __init__(self):
        # Get the config object from the microservice
        response = requests.get("http://localhost:8421/get_config")
        if response.status_code == 200:
            # Parse BSON response
            bson_data = response.content
            self.config = bson.loads(bson_data)
        else:
            raise Exception("Failed to fetch config object from microservice.")
         
        self.MODEL = SentenceTransformer(self.config['models']['embedding_model'])

    def get_embedding(self, text):
        embedding = self.MODEL.encode(text).tobytes()
        return embedding

# Create an instance of the remote service
embedding_service = EmbeddingService.remote()
