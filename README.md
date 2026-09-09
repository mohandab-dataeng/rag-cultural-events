# 🎭 rag-cultural-events

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.4-1C3C3C?logo=langchain&logoColor=white)
![Mistral AI](https://img.shields.io/badge/Mistral%20AI-mistral--small-FA520F?logo=mistralai&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-CPU-0467DF?logo=meta&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?logo=uv&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-tested-0A9EDC?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

**POC d'un chatbot RAG (Retrieval-Augmented Generation) qui aide à découvrir des événements culturels en Île-de-France, en langage naturel.**

## Le principe

Poser une question en langage naturel — *"des expos photo cette semaine ?"*, *"un événement à Antony le 10 septembre ?"* — et obtenir une réponse ancrée dans de vraies données d'événements, avec les sources utilisées affichées à côté. Pas de réponse inventée : si l'info n'est pas dans la base, le chatbot le dit clairement plutôt que d'halluciner.

## Comment ça marche

```
Open Agenda API → nettoyage/filtrage → chunking → embeddings (Mistral) → index FAISS
                                                                              ↓
                                          question utilisateur → recherche de similarité → LLM (Mistral) → réponse + sources
```

1. **Collecte** — récupération des événements via l'API Open Agenda, sur un agenda officiel Île-de-France
2. **Nettoyage** — filtrage strict sur les événements de moins d'un an, gestion des champs manquants
3. **Chunking** — fusion titre + description + lieu + dates en un texte cohérent par événement
4. **Vectorisation** — chaque chunk transformé en embedding via Mistral, indexé dans FAISS
5. **Génération** — au moment de la question, FAISS retrouve les événements les plus pertinents, Mistral rédige la réponse en s'appuyant uniquement sur ce contexte

## Stack technique

| Outil | Rôle |
|---|---|
| **LangChain** (`langchain_core`, LCEL) | Orchestration du pipeline RAG |
| **Mistral AI** (`mistral-embed`, `mistral-small-latest`) | Embeddings + génération de réponses |
| **FAISS** (CPU) | Base de données vectorielle, recherche par similarité |
| **Open Agenda API** | Source de données événementielles |
| **Python 3.13** + **uv** | Langage et gestion des dépendances |
| **pytest** | Tests unitaires |

## Structure du projet

```
rag-cultural-events/
├── src/
│   ├── data_collection.py   # Collecte des événements via Open Agenda
│   ├── preprocessing.py      # Nettoyage, filtrage, chunking
│   ├── vectorization.py      # Embeddings + construction de l'index FAISS
│   ├── rag_chain.py          # Chatbot : retrieval + génération
│   └── evaluate.py           # Évaluation sur un jeu de questions annoté
├── tests/
│   └── test_data_filters.py  # Vérifie la conformité des données (date, ville)
├── data/
│   ├── raw/                  # Événements bruts collectés
│   ├── processed/            # Événements nettoyés et chunkés
│   └── qa_test_set.json      # Jeu de questions de test
├── index_faiss/               # Index vectoriel (généré, non versionné)
├── .env.example                # Template des clés API
├── pyproject.toml
└── README.md
```

## Installation

Prérequis : Python 3.13+, [uv](https://docs.astral.sh/uv/), une clé API [Mistral](https://console.mistral.ai) et une clé publique [Open Agenda](https://openagenda.com/api).

```bash
git clone https://github.com/<ton-username>/rag-cultural-events.git
cd rag-cultural-events

uv sync

cp .env.example .env
# renseigner MISTRAL_API_KEY et OPENAGENDA_PUBLIC_KEY dans .env
```

## Reconstruire la base de données à partir de zéro

Le pipeline est entièrement reproductible, dans cet ordre :

```bash
uv run python src/data_collection.py    # collecte les événements Open Agenda
uv run python src/preprocessing.py      # nettoie et prépare les données
uv run python src/vectorization.py      # construit l'index FAISS
```

## Lancer le chatbot

```bash
uv run python src/rag_chain.py
```

```
Question : Quels événements à Issy-les-Moulineaux en octobre ?
Réponse : ...
Sources :
  - La voile de confiance (Issy-les-Moulineaux)
  - ...
```

## Lancer les tests

```bash
uv run pytest tests/ -v
```

Vérifie que chaque événement indexé a bien une date de moins d'un an, un titre, une description et une ville renseignée.

## Évaluer le chatbot

Un jeu de questions annotées (`data/qa_test_set.json`) permet de vérifier la qualité des réponses générées face aux événements réels de la base :

```bash
uv run python src/evaluate.py
```

## Limites connues et pistes d'amélioration

- **Adresse précise non incluse dans le texte vectorisé** — seule la ville l'est ; une évolution consisterait à l'ajouter au chunk pour permettre des réponses plus précises
- **`langchain-community`** (utilisé pour l'intégration FAISS) est en fin de vie — à surveiller pour une migration future vers un package dédié maintenu
- **Évaluation manuelle** — une version industrialisée gagnerait à s'appuyer sur un framework standard type [RAGAS](https://github.com/explodinggradients/ragas) (faithfulness, context precision/recall, answer relevancy) plutôt qu'une vérification manuelle
- **Tier gratuit Mistral** — limites de débit basses, non adaptées à un usage multi-utilisateurs en production ; un passage en tier payant serait nécessaire pour un déploiement à plus grande échelle