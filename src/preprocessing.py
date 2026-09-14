"""
Nettoyage et structuration des événements Open Agenda avant vectorisation.
"""
import json
from datetime import datetime, timedelta, timezone


def load_raw_events(filepath="data/raw/events_raw.json"):
    """
    Charge les événements bruts collectés depuis Open Agenda.

    Args:
        filepath (str): chemin du fichier JSON contenant les événements bruts.

    Returns:
        list[dict]: liste des événements bruts tels que retournés par l'API.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def is_valid_event(event, date_limite):
    """
    Vérifie qu'un événement respecte les contraintes métier du projet.

    Un événement est valide s'il possède un titre et une description en
    français, une date de début, et si cette date de début est postérieure
    à date_limite (contrainte "moins d'un an").

    Args:
        event (dict): événement brut Open Agenda.
        date_limite (datetime): date en dessous de laquelle un événement
            est considéré comme trop ancien.

    Returns:
        bool: True si l'événement respecte toutes les contraintes, False sinon.
    """
    titre = event.get("title", {}).get("fr")
    description = event.get("description", {}).get("fr")
    if not titre or not description:
        return False

    begin = event.get("firstTiming", {}).get("begin")
    if not begin:
        return False

    begin_date = datetime.fromisoformat(begin)
    if begin_date < date_limite:
        return False

    return True


def clean_event(event):
    """
    Extrait et restructure les champs utiles d'un événement brut.

    Ne fait aucune validation : suppose que l'événement a déjà été validé
    par is_valid_event. Applique une valeur par défaut si la ville est absente.

    Args:
        event (dict): événement brut Open Agenda, déjà validé.

    Returns:
        dict: événement nettoyé avec les clés uid, title, description,
            city, address, begin, end.
    """
    location = event.get("location", {})
    return {
        "uid": event.get("uid"),
        "title": event["title"]["fr"],
        "description": event["description"]["fr"],
        "city": location.get("city") or "Ville non précisée",
        "address": location.get("address", ""),
        "begin": event.get("firstTiming", {}).get("begin", ""),
        "end": event.get("lastTiming", {}).get("end", ""),
    }


def build_chunk_text(cleaned_event):
    """
    Fusionne les champs d'un événement nettoyé en un seul bloc de texte.

    Ce texte (chunk_text) est la seule donnée envoyée à Mistral Embed pour
    la vectorisation : fusionner titre, description, lieu et dates permet
    à FAISS de matcher une question quel que soit son angle (thème, ville
    ou date). C'est la clé la plus importante pour le LLM.

    Args:
        cleaned_event (dict): événement nettoyé, sortie de clean_event.

    Returns:
        str: texte fusionné prêt pour la vectorisation.
    """
    return (
        f"{cleaned_event['title']}. {cleaned_event['description']} "
        f"Lieu : {cleaned_event['city']}. "
        f"Du {cleaned_event['begin']} au {cleaned_event['end']}."
    )


def preprocess_events(raw_events):
    """
    Orchestre le nettoyage complet d'une liste d'événements bruts.

    Calcule une seule fois la date_limite (aujourd'hui - 1 an), puis pour
    chaque événement brut : filtre avec is_valid_event, nettoie avec
    clean_event, et ajoute le chunk_text avec build_chunk_text.

    Args:
        raw_events (list[dict]): événements bruts Open Agenda.

    Returns:
        list[dict]: événements valides, nettoyés, chacun enrichi d'une
            clé "chunk_text".
    """
    date_limite = datetime.now(timezone.utc) - timedelta(days=365)
    processed = []
    for event in raw_events:
        if not is_valid_event(event, date_limite):
            continue
        cleaned = clean_event(event)
        cleaned["chunk_text"] = build_chunk_text(cleaned)
        processed.append(cleaned)
    return processed


def save_processed_data(events, filepath="data/processed/events_clean.json"):
    """
    Sauvegarde les événements nettoyés au format JSON.

    Args:
        events (list[dict]): événements nettoyés, sortie de preprocess_events.
        filepath (str): chemin de sortie du fichier JSON.

    Returns:
        None
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    raw = load_raw_events()
    print(f"{len(raw)} événements bruts chargés.")
    processed = preprocess_events(raw)
    print(f"{len(processed)} événements valides après nettoyage.")
    save_processed_data(processed)
    print("Sauvegardé dans data/processed/events_clean.json")