import json
from pathlib import Path

fake_users_db = json.loads(Path(__file__).parent.joinpath("fake_users.json").read_text())
