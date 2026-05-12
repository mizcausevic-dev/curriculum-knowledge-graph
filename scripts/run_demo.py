from __future__ import annotations

from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.graph_service import build_service


def main() -> None:
    print(json.dumps(build_service().sample_payload(), indent=2))


if __name__ == "__main__":
    main()
