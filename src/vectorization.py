"""
Vectorisation des événements et construction de l'index FAISS.
Utilise le wrapper LangChain (gère automatiquement la correspondance vecteur <-> métadonnées).
"""
import json
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()


def load_processed_events(filepath="data/processed/events_clean.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def build_documents(events):
    """Transforme chaque événement en objet Document LangChain (texte + métadonnées)."""
    documents = []
    for event in events:
        doc = Document(
            page_content=event["chunk_text"],
            metadata={
                "uid": event["uid"],
                "title": event["title"],
                "city": event["city"],
                "address": event["address"],
                "begin": event["begin"],
                "end": event["end"],
            },
        )
        documents.append(doc)
    return documents


def build_vector_store(documents):
    """Calcule les embeddings et construit l'index FAISS."""
    embeddings = MistralAIEmbeddings(
        model="mistral-embed",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
    )
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store


def save_vector_store(vector_store, path="index_faiss"):
    vector_store.save_local(path)


if __name__ == "__main__":
    events = load_processed_events()
    print(f"{len(events)} événements chargés.")

    documents = build_documents(events)
    print("Documents LangChain construits.")

    print("Calcul des embeddings et construction de l'index FAISS (peut prendre plusieurs minutes)...")
    vector_store = build_vector_store(documents)

    save_vector_store(vector_store)
    print("Index FAISS sauvegardé dans index_faiss/")