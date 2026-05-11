import json
from pathlib import Path
from typing import Dict, List

class TicketStore:
    def __init__(self, json_path: Path) -> None:
        self.json_path = json_path

    def load(self) -> List[Dict]:
        if self.json_path.exists():
            with open(self.json_path, "r", encoding = "utf-8") as f:
                return json.load(f)
        else:
            return []
    def save(self, tickets: List[Dict]):
        with open(self.json_path, "w", encoding ="utf-8") as f:
            json.dump(tickets, f, indent = 4, default = str)