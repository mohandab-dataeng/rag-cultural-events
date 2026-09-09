"""
Nettoyage et structuration des événements Open Agenda avant vectorisation.
"""
import json
from datetime import datetime, timedelta, timezone

def load_raw_events(filepath="data/raw/events_raw.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def is_valid_event(event, date_limite):
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
    return (
        f"{cleaned_event['title']}. {cleaned_event['description']} "
        f"Lieu : {cleaned_event['city']}. "
        f"Du {cleaned_event['begin']} au {cleaned_event['end']}."
    )

def preprocess_events(raw_events):
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
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    raw = load_raw_events()
    print(f"{len(raw)} événements bruts chargés.")
    processed = preprocess_events(raw)
    print(f"{len(processed)} événements valides après nettoyage.")
    save_processed_data(processed)
    print("Sauvegardé dans data/processed/events_clean.json")