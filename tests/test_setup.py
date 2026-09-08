"""
Script de vérification de l'environnement.
Teste  les librairies critiques, les clés API sont bien chargées depuis .env.
"""
import os
from dotenv import load_dotenv

# --- 1 : Charger les variables d'environnement depuis .env ---
load_dotenv()

# --- 2 : Imports des librairies indispensable ---
import langchain
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
import faiss
import pandas as pd
import requests

# --- 3. Verification d'accès des clés API
def check_env_variables():
    mistral_key = os.getenv("MISTRAL_API_KEY")
    openagenda_key = os.getenv("OPENAGENDA_PUBLIC_KEY")
    
    assert mistral_key is not None, "MISTRAL_API_KEY manquante dans .env"
    assert openagenda_key is not None, "OPENAGENDA_PUBLIC_KEY manquante dans .env" 

    print("Clés API trouvées :)")


# --- 4. Verification que faiss tourne correctement en mode cpu
def check_faiss_cpu():
    nb_gpus = faiss.get_num_gpus()
    assert nb_gpus == 0, f"FAISS détecte {nb_gpus} GPU(s), la version CPU est attendue"
    print(f"FAISS en mode CPU confirmé (GPUs détectés : {nb_gpus}) ✓")


if __name__ == "__main__":
    print("Vérification de l'environnement...")
    check_env_variables()
    check_faiss_cpu()
    print("Tout est OK !")