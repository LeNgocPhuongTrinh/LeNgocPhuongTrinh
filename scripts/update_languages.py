"""Refresh an honest snapshot of language bytes in owned public non-fork repos."""

import json
import os
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "LeNgocPhuongTrinh"


def get_json(url: str) -> dict | list:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-readme"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return json.load(response)


def collect_languages() -> tuple[Counter, int]:
    totals = Counter()
    repository_count = 0
    page = 1
    while True:
        repositories = get_json(
            f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}"
        )
        for repository in repositories:
            if not repository["fork"]:
                totals.update(get_json(repository["languages_url"]))
                repository_count += 1
        if len(repositories) < 100:
            return totals, repository_count
        page += 1


def render_chart(totals: Counter, date: str, count: int) -> str:
    total_bytes = sum(totals.values())
    rows = totals.most_common()
    height = 105 + 48 * max(len(rows), 1)
    content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="{height}" viewBox="0 0 640 {height}">',
        f'<rect width="640" height="{height}" fill="#f7f4ed"/>',
        '<g font-family="monospace" fill="#17191c">',
        '<text x="24" y="32" font-size="18">MOST USED LANGUAGES</text>',
        f'<text x="24" y="55" font-size="11">{count} public non-fork repositories · bytes of code · {date}</text>',
    ]
    for index, (language, value) in enumerate(rows):
        y = 82 + index * 48
        percentage = value / total_bytes * 100
        content.extend([
            f'<text x="24" y="{y + 13}" font-size="14">{escape(language)}</text>',
            f'<rect x="210" y="{y}" width="310" height="12" fill="#e5dfd8"/>',
            f'<rect x="210" y="{y}" width="{percentage * 3.1:.2f}" height="12" fill="#d50920"/>',
            f'<text x="605" y="{y + 12}" text-anchor="end" font-size="14">{percentage:.1f}%</text>',
            f'<text x="605" y="{y + 30}" text-anchor="end" font-size="11">{value:,} bytes</text>',
        ])
    if not total_bytes:
        content.append('<text x="24" y="90" font-size="14">No language bytes reported.</text>')
    return "\n".join(content + ["</g></svg>\n"])


def main() -> None:
    totals, count = collect_languages()
    date = datetime.now(timezone.utc).date().isoformat()
    # Fetch everything successfully before replacing the last good snapshot.
    snapshot = {
        "as_of": date,
        "source": f"https://api.github.com/users/{USERNAME}/repos",
        "measurement": "Sum of GitHub languages API byte counts across owned public non-fork repositories",
        "repository_count": count,
        "total_bytes": sum(totals.values()),
        "language_bytes": dict(totals),
    }
    (ROOT / "assets/languages.svg").write_text(render_chart(totals, date, count), encoding="utf-8")
    (ROOT / "assets/languages.json").write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
