"""
Tests unitaires : vérifient que les données indexées respectent les contraintes du cahier des charges
- Événements de moins d'un an
- Événements en Île-de-France (garanti par l'agenda source choisi)
"""
import json
from datetime import datetime, timedelta, timezone
import pytest

DATA_PATH = "data/processed/events_clean.json"


@pytest.fixture(scope="module")
def events():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_events_not_empty(events):
    assert len(events) > 0


def test_all_events_have_required_fields(events):
    for event in events:
        assert event.get("title")
        assert event.get("description")
        assert event.get("chunk_text")


def test_all_events_less_than_one_year(events):
    date_limite = datetime.now(timezone.utc) - timedelta(days=365)
    for event in events:
        begin_str = event.get("begin")
        assert begin_str, f"Événement {event.get('uid')} sans date de début"
        begin_date = datetime.fromisoformat(begin_str)
        assert begin_date >= date_limite, f"Événement {event.get('uid')} trop ancien : {begin_date}"


def test_all_events_have_city(events):
    for event in events:
        assert event.get("city"), f"Événement {event.get('uid')} sans ville renseignée"