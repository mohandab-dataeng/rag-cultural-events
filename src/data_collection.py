"""
Collecte des événements culturels via l'API Open Agenda.
Filtre : Île-de-France, événements des 12 derniers mois.
"""

import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.openagenda.com/v2/agendas/56500817/events"
REGION = "Île-de-France"

def build_params(after_cursor=None):
    """Construit les paramètres de requête pour l'API Open Agenda."""
    date_limite = (datetime.now() - timedelta(days=365)).isoformat()

    params = {
        "key": os.getenv("OPENAGENDA_PUBLIC_KEY"),
        "timings[gte]": date_limite,
        "relative[]": ["upcoming", "current"], # <- Filtre de la nomenclature exigée pour openagenda
        "size": 300,
    }
    # Retourne le marque-page
    if after_cursor:
        params["after[]"] = after_cursor
 
    return params

def fetch_all_events():
    """Récupère tous les événements en paginant avec le curseur 'after'."""
    all_events = []
    after_cursor = None

    while True:
        # faire l'appel GET avec requests, récupérer le JSON
        params = build_params(after_cursor)
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        # ajouter les events de cette page à all_events
        all_events.extend(data["events"])
        
        print(f"Page récupérée : {len(all_events)} / {data.get('total', '?')} événements")

        # Vérifier si 'after' dans la réponse est None -> stop
        # sinon mettre à jour after_cursor pour la prochaine itération
        if data["after"] is None:
            break
        else: 
            after_cursor = data["after"]
    return all_events

def save_raw_data(events, filepath="data/raw/events_raw.json"):
    """Sauvegarde les événements bruts en JSON."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print(f"Collecte des événements pour {REGION}...")
    events = fetch_all_events()
    print(f"{len(events)} événements récupérés.")
    save_raw_data(events)
    print("Données sauvegardées dans data/raw/events_raw.json")