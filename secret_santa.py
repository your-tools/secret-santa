import secrets
import random
import shutil
import sys
from pathlib import Path


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


def gen_html(
    input_path: Path, output_path: Path, id: str, author: str, recipient: str
) -> None:
    out_html_path = output_path / f"{id}.html"
    input_html = (input_path / "template.html").read_text()
    # fmt: off
    output_html = (
        input_html
            .replace("{{ author }}", author)
            .replace("{{ recipient }}", recipient)
    )
    # fmt: on
    out_html_path.write_text(output_html)


def copy_assets(input_path: Path, output_path: Path) -> None:
    for asset in input_path.glob("*"):
        shutil.copy(asset, output_path)


def gen_spoiler(output_path: Path, pairs: list[tuple[str, str]]) -> None:
    spoiler_text = output_path / "spoiler.txt"
    for author, recipient in pairs.items():
        with spoiler_text.open("a") as stream:
            stream.write(f"{author}: {recipient}\n")


def main() -> None:
    output_path = Path("output")
    input_path = Path("input")
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir()
    copy_assets(input_path, output_path)
    participants = sys.argv[1:]
    pairs = draw_pairs(participants)
    gen_spoiler(output_path, pairs)
    for author, recipient in pairs.items():
        id = secrets.token_hex(3)
        gen_html(input_path, output_path, str(id), author, recipient)


if __name__ == "__main__":
    main()
