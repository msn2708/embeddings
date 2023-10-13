import ray
from sentence_transformers import SentenceTransformer
import bson
import requests

ray.init()

@ray.remote
class EmbeddingService:
    def __init__(self):
        try:
            # Get the config object from the microservice
            response = requests.get("http://localhost:8421/get_config")
            if response.status_code == 200:
                # Parse BSON response
                self.config = bson.loads(response.content)
            else:
                raise Exception (f"Failed to fetch config object from microservice: {response.status_code}/{response.reason}")
        except Exception as e:
           raise Exception(f"An error occured when loading the config object: {e.with_traceback}")
         
        self.MODEL = SentenceTransformer(self.config['models']['embedding_model'])

    def get_embedding(self, text):
        embedding = None
        try:
            embedding = self.MODEL.encode(text).tobytes()
            return embedding
        except Exception as e:
            raise Exception (f"Error trying to embed text: {e.with_traceback}")

# Create an instance of the remote service
embedding_service = EmbeddingService.remote()
