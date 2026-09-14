from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

text = "Express shipping usually takes 1 to 2 business days."

vector = embeddings.embed_query(text)
print("Vector length:", len(vector))
print("First 10 values:", vector[:10])