"""
Pipeline principal RAG — orchestre l'ensemble du système :
1. Collecte des données Open Agenda
2. Nettoyage et chunking
3. Vectorisation et construction de l'index FAISS
4. Lancement des tests unitaires
5. Lancement du chatbot interactif
"""
import subprocess
import sys


def run_step(description, command):
    """Exécute une étape du pipeline et arrête tout si elle échoue."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"\n❌ ÉCHEC : {description}")
        sys.exit(1)
    print(f"\n✅ {description} — terminé")


if __name__ == "__main__":
    print("🎭 Pipeline RAG — rag-cultural-events")
    print("=" * 60)

    # Phase 1 — Construction de la base vectorielle (exécutée une seule fois ou sur demande)
    run_step(
        "Étape 1/4 — Collecte des événements Open Agenda",
        "uv run python src/data_collection.py"
    )

    run_step(
        "Étape 2/4 — Nettoyage et structuration des données",
        "uv run python src/preprocessing.py"
    )

    run_step(
        "Étape 3/4 — Vectorisation et construction de l'index FAISS",
        "uv run python src/vectorization.py"
    )

    # Phase 2 — Validation
    run_step(
        "Étape 4/4 — Tests unitaires",
        "uv run pytest tests/test_data_filters.py -v"
    )

    # Phase 3 — Chatbot interactif
    print(f"\n{'='*60}")
    print("  🚀 Pipeline terminé — lancement du chatbot")
    print(f"{'='*60}\n")
    subprocess.run("uv run python src/rag_chain.py", shell=True)