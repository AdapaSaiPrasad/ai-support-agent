from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from rank_bm25 import BM25Okapi

from app.rag.loader import load_documents

VECTORSTORE_PATH = Path("app/rag/faiss_index")
# Number of candidates retrieved from FAISS
TOP_K = 4
# Keep only results whose FAISS distance is below this value.
# This is a starting value and should be tuned using evaluation data.
SIMILARITY_THRESHOLD = 0.7
def create_vectorstore():
    chunks = load_documents()
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )
    vectorstore.save_local(VECTORSTORE_PATH)
    return vectorstore

def load_vectorstore():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )
    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def retrieve_chunks(question):

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search_with_score(
        question,
        k=TOP_K
    )
    print("\n===== RETRIEVAL =====")

    for document, score in results:
        print(f"\nScore: {score}")
        print(document.page_content)

    return results

def check_relevance(results):
    relevant_results = [
        (document, score)
        for document, score in results
        if score <= SIMILARITY_THRESHOLD
    ]
    return relevant_results

def generate_answer(question, relevant_results):

    context = "\n\n".join(
        document.page_content
        for document, score in relevant_results
    )
    prompt = f"""
You are an AI customer support agent.
Answer the user's question using only the provided context.
If the answer cannot be determined from the context,
say that you do not have enough information.
Context:
{context}
Question:
{question}
Answer:
"""
    llm = ChatOllama(
        model="qwen2.5:0.5b"
    )
    response = llm.invoke(prompt)

    return response.content

def rag_answer(question):
    # 1. Retrieve candidate chunks
    results = retrieve_chunks(question)

    # 2. Check whether retrieved chunks are relevant
    relevant_results = check_relevance(results)

    print("\n===== RELEVANCE CHECK =====")
    print(f"Retrieved chunks: {len(results)}")
    print(f"Relevant chunks: {len(relevant_results)}")

    # 3. Fallback if nothing is relevant
    if not relevant_results:
        return (
            "I don't have enough information in the "
            "company knowledge base to answer that question."
        )

    # 4. Generate grounded answer
    return generate_answer(question, relevant_results)


if __name__ == "__main__":

    question = input("Ask your question: ")

    answer = rag_answer(question)

    print("\n===== FINAL ANSWER =====")
    print(answer)