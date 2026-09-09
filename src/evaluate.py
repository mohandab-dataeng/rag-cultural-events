"""
Fait tourner le RAG sur tes questions réelles, affiche la réponse générée à côté du titre attendu.
"""
import json
import time
from rag_chain import load_vector_store, build_rag_chain, ask_question


def load_qa_set(filepath="data/qa_test_set.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def run_evaluation(qa_set, retriever, generation_chain):
    results = []
    for qa in qa_set:
        print(f"Question {qa['id']} : {qa['question']}")
        reponse, sources = ask_question(retriever, generation_chain, qa["question"])
        print(f"  Réponse générée : {reponse}")
        print(f"  Événement attendu : {qa['source_title']}")
        print(f"  Sources trouvées  : {[doc.metadata['title'] for doc in sources]}\n")

        results.append({
            "id": qa["id"],
            "question": qa["question"],
            "source_title_attendu": qa["source_title"],
            "reponse_generee": reponse,
            "sources_trouvees": [doc.metadata["title"] for doc in sources],
        })
        time.sleep(1.5)
    return results


def save_results(results, filepath="data/qa_evaluation_results.json"):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print("Chargement de l'index FAISS...")
    vector_store = load_vector_store()
    retriever, generation_chain = build_rag_chain(vector_store)

    qa_set = load_qa_set()
    print(f"{len(qa_set)} questions à évaluer.\n")

    results = run_evaluation(qa_set, retriever, generation_chain)
    save_results(results)
    print("Résultats sauvegardés dans data/qa_evaluation_results.json")