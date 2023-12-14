import secrets
import random
import shutil
import sys
from pathlib import Path
from uuid import uuid4


def _draw_pairs(participants: list[str]) -> dict[str, str] | None:
    result: dict[str, str] = {}
    for author in participants:
        recipients_so_far = result.values()
        available_recipients = [
            p for p in participants if p != author and p not in recipients_so_far
        ]
        if not available_recipients:
            return None
        recipient = random.choice(available_recipients)
        result[author] = recipient
    return result


def draw_pairs(participants: list[str]) -> dict[str, str]:
    while True:
        pairs = _draw_pairs(participants)
        if pairs:
            return pairs


def gen_html(out_path: Path, id: str, author: str, recipient: str) -> None:
    html_path = out_path / f"{id}.html"
    template = (
        Path("template.html")
        .read_text()
        .replace("{{ author }}", author)
        .replace("{{ recipient }}", recipient)
    )
    html_path.write_text(template)
    print(html_path)


def main() -> None:
    out_path = Path("out")
    if out_path.exists():
        shutil.rmtree(out_path)
    out_path.mkdir()
    participants = sys.argv[1:]
    pairs = draw_pairs(participants)
    for author, recipient in pairs.items():
        id = secrets.token_hex(3)
        gen_html(out_path, str(id), author, recipient)


if __name__ == "__main__":
    main()
