"""
Nettoyage et structuration des événements Open Agenda avant vectorisation.
- Filtre de sécurité : événements < 1 an (redondant avec le filtre API)
- Nettoyage des champs manquants
- Un "chunk" = un texte structuré par événement (titre + description + lieu + dates)
"""
import json
from datetime import datetime, timedelta, timezone

# ============================================================
# BOÎTE À OUTILS — syntaxe générique, à réutiliser ci-dessous
# ============================================================
# Accès sécurisé à un dict :              dictionnaire.get("cle", valeur_par_defaut)
# Accès sécurisé à un dict imbriqué :     dictionnaire.get("cle1", {}).get("cle2")
# Sortir d'une fonction avec un résultat: return quelque_chose
# String ISO -> objet date :              datetime.fromisoformat(une_chaine)
# Comparer deux dates :                   if date_a < date_b:
# Construire un dict :                    {"cle_a": valeur_a, "cle_b": valeur_b}
# f-string (texte + variables) :          f"Voici {variable_a} et {variable_b}."
# Boucler en sautant certains éléments :  for e in liste: \n    if cond: continue
# Ajouter à une liste :                   ma_liste.append(element)
# Date "il y a N jours" (UTC) :           datetime.now(timezone.utc) - timedelta(days=365)
# Lire un JSON :                          with open(chemin, "r", encoding="utf-8") as f: json.load(f)
# Écrire un JSON :                        with open(chemin, "w", encoding="utf-8") as f: json.dump(obj, f, indent=2, ensure_ascii=False)
# ============================================================

# 
def load_raw_events(filepath="data/raw/events_raw.json"):
    """Charge les événements bruts collectés."""
    with open(filepath, "r", encoding="utf-8") as f: 
        raw_events = json.load(f)
    return raw_events


def is_valid_event(event, date_limite):
    """Un événement est valide s'il a un titre, une description, et une date de début < 1 an.
    Champs disponibles dans `event` : title.fr, description.fr, firstTiming.begin
    """
    
    pass

def clean_event(event):
    """Extrait uniquement les champs utiles : uid, title, description, city, address, begin, end.
    Champs disponibles : uid, title.fr, description.fr, location.city, location.address,
    firstTiming.begin, lastTiming.end
    """
    pass

def build_chunk_text(cleaned_event):
    """Construit le texte final qui sera transformé en embedding, à partir des champs de cleaned_event."""
    pass

def preprocess_events(raw_events):
    """Filtre, nettoie et chunk tous les événements bruts. Retourne la liste des événements traités."""
    pass

def save_processed_data(events, filepath="data/processed/events_clean.json"):
    """Sauvegarde les événements nettoyés."""
    pass


if __name__ == "__main__":
    raw = load_raw_events()
    print(f"{len(raw)} événements bruts chargés.")
    processed = preprocess_events(raw)
    print(f"{len(processed)} événements valides après nettoyage.")
    save_processed_data(processed)
    print("Sauvegardé dans data/processed/events_clean.json")