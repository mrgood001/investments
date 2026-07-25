import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = BASE_DIR / "data" / "user_settings.json"

# Создать папку data, если ее нет
SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_commission_rate() -> float | None:
    if not SETTINGS_PATH.exists():
        return None  # сигнал GUI спросить у юзера

    with SETTINGS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f).get("commission_rate")


def save_commission_rate(rate: float):
    with SETTINGS_PATH.open("w", encoding="utf-8") as f:
        json.dump({"commission_rate": rate}, f, indent=4)