import pytest
from ornament.rag.vector_store import LocalVectorStore

def test_rag_vector_store():
    store = LocalVectorStore()
    store.add_document("doc1", "Next.js routing", "Next.js", "App Router links must match folders in app/ like /contact.")
    store.add_document("doc2", "Tailwind dark mode", "Tailwind", "Tailwind dark mode requires dark class on html.")

    results = store.search("how do routes work in nextjs?", top_k=1)
    assert len(results) == 1
    assert results[0]["id"] == "doc1"
    assert "routing" in results[0]["title"].lower()
