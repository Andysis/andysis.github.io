"""Collect GitHub star counts for repository links used on the home page."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


SOURCE_PATH = Path("_pages/about.md")
OUTPUT_PATH = Path("_data/github_stars.json")
GITHUB_REPOSITORY_URL = re.compile(
    r"https://github\.com/([^/\s)\]#?]+)/([^/\s)\]#?,]+)", re.IGNORECASE
)


def find_repositories(markdown: str) -> list[str]:
    repositories = set()
    for owner, name in GITHUB_REPOSITORY_URL.findall(markdown):
        name = name.rstrip(".;:")
        if name.endswith(".git"):
            name = name[:-4]
        if owner and name:
            repositories.add(f"{owner}/{name}")
    return sorted(repositories, key=str.casefold)


def load_existing() -> dict[str, int]:
    if not OUTPUT_PATH.exists():
        return {}
    data = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{OUTPUT_PATH} must contain a JSON object")
    return {
        repo: stars
        for repo, stars in data.items()
        if isinstance(repo, str) and isinstance(stars, int) and stars >= 0
    }


def fetch_stars(repository: str, token: str) -> int:
    url = "https://api.github.com/repos/" + quote(repository, safe="/")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "andysis-github-stars-workflow",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url, headers=headers)
    with urlopen(request, timeout=20) as response:
        data = json.load(response)
    stars = data.get("stargazers_count")
    if not isinstance(stars, int):
        raise ValueError(f"GitHub returned no star count for {repository}")
    return stars


def main() -> int:
    repositories = find_repositories(SOURCE_PATH.read_text(encoding="utf-8"))
    if not repositories:
        raise RuntimeError(f"No GitHub repository links found in {SOURCE_PATH}")

    token = os.environ.get("GITHUB_TOKEN", "")
    existing = load_existing()
    updated: dict[str, int] = {}
    missing: list[str] = []

    for repository in repositories:
        try:
            updated[repository] = fetch_stars(repository, token)
            print(f"{repository}: {updated[repository]}")
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            if repository in existing:
                updated[repository] = existing[repository]
                print(
                    f"warning: {repository}: {exc}; keeping {existing[repository]}",
                    file=sys.stderr,
                )
            else:
                missing.append(repository)
                print(f"error: {repository}: {exc}", file=sys.stderr)

    if missing:
        print(
            "No previous data is available for: " + ", ".join(missing),
            file=sys.stderr,
        )
        return 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(updated, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(updated)} repositories to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
