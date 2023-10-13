from ray import serve
from embedding_service import EmbeddingService

serve.start(http_port=9410)

# Register the endpoint with Ray Serve
serve.create_endpoint("embedding_service", route="/get_embedding")

# Define the Ray Serve backend
serve.create_backend("embedding_backend", EmbeddingService)

# Link the endpoint with the backend
serve.link("embedding_service", "embedding_backend")

# Start the Ray Serve app
serve.get_handle("embedding_service").block_until_ready()

print("Ray Serve API is ready.")
