from datetime import datetime
import json
import multiprocessing as mp
import os
import re
import time
from urllib.error import URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from scholarly import scholarly


RESULTS_DIR = "results"
GS_DATA = "gs_data.json"
SHIELDS_DATA = "gs_data_shieldsio.json"
FETCH_TIMEOUT = int(os.environ.get("SCHOLAR_FETCH_TIMEOUT", "75"))
MAX_ATTEMPTS = int(os.environ.get("SCHOLAR_MAX_ATTEMPTS", "2"))
RETRY_BASE_SECONDS = int(os.environ.get("SCHOLAR_RETRY_BASE_SECONDS", "15"))
DIRECT_TIMEOUT = int(os.environ.get("SCHOLAR_DIRECT_TIMEOUT", "20"))
SCHOLAR_PROFILE_URL = "https://scholar.google.com/citations"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)


class FetchTimeoutError(Exception):
    pass


def norm_title(s):
    return s.lower().replace("\n", " ").replace("\r", " ").strip()


def parse_number(value):
    digits = re.sub(r"[^0-9]", "", value or "")
    return int(digits) if digits else 0


def parse_profile_html(html):
    """Parse the public profile page without making per-publication requests."""
    soup = BeautifulSoup(html, "html.parser")
    name_node = soup.select_one("#gsc_prf_in")
    if name_node is None:
        raise RuntimeError("Scholar returned a block/consent page instead of a profile")

    author = {
        "name": name_node.get_text(" ", strip=True),
        "affiliation": "",
        "interests": [],
        "cites_per_year": {},
        "publications": [],
        "data_source": "google_scholar_profile_html",
    }

    affiliation = soup.select_one("#gsc_prf_i .gsc_prf_il")
    if affiliation:
        author["affiliation"] = affiliation.get_text(" ", strip=True)
    author["interests"] = [
        node.get_text(" ", strip=True) for node in soup.select("#gsc_prf_int a")
    ]

    metric_names = ("citedby", "hindex", "i10index")
    metric_rows = soup.select("#gsc_rsb_st tbody tr")
    for metric_name, row in zip(metric_names, metric_rows):
        cells = row.select("td.gsc_rsb_std")
        author[metric_name] = parse_number(cells[0].get_text()) if cells else 0
        author[f"{metric_name}5y"] = (
            parse_number(cells[1].get_text()) if len(cells) > 1 else 0
        )

    years = [node.get_text(strip=True) for node in soup.select(".gsc_g_t")]
    counts = [parse_number(node.get_text()) for node in soup.select(".gsc_g_al")]
    author["cites_per_year"] = {
        int(year): count
        for year, count in zip(years, counts)
        if year.isdigit()
    }

    for row in soup.select("tr.gsc_a_tr"):
        title_node = row.select_one("a.gsc_a_at")
        if title_node is None:
            continue

        detail_lines = row.select(".gs_gray")
        href = title_node.get("href", "")
        query = parse_qs(urlparse(href).query)
        author_pub_id = query.get("citation_for_view", [""])[0]
        year_node = row.select_one(".gsc_a_y span")
        cited_node = row.select_one(".gsc_a_c a")
        bib = {
            "title": title_node.get_text(" ", strip=True),
            "author": detail_lines[0].get_text(" ", strip=True)
            if detail_lines
            else "",
            "citation": detail_lines[1].get_text(" ", strip=True)
            if len(detail_lines) > 1
            else "",
            "pub_year": year_node.get_text(strip=True) if year_node else "",
        }
        publication = {
            "container_type": "Publication",
            "source": "AUTHOR_PUBLICATION_ENTRY",
            "bib": bib,
            "filled": False,
            "num_citations": parse_number(cited_node.get_text()) if cited_node else 0,
        }
        if author_pub_id:
            publication["author_pub_id"] = author_pub_id
        author["publications"].append(publication)

    if not author["publications"]:
        raise RuntimeError("Scholar profile contained no publication rows")
    return author


def fetch_profile_direct():
    params = urlencode(
        {
            "user": os.environ["GOOGLE_SCHOLAR_ID"],
            "hl": "en",
            "pagesize": 100,
        }
    )
    request = Request(
        f"{SCHOLAR_PROFILE_URL}?{params}",
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urlopen(request, timeout=DIRECT_TIMEOUT) as response:
        return parse_profile_html(response.read().decode("utf-8", errors="replace"))


def fetch_author_scholarly():
    author = scholarly.search_author_id(os.environ["GOOGLE_SCHOLAR_ID"])
    scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])
    author["data_source"] = "scholarly"
    return author


def fetch_worker(queue):
    try:
        queue.put(("ok", fetch_author_scholarly()))
    except Exception as exc:
        queue.put(("error", repr(exc)))


def fetch_with_timeout(seconds):
    queue = mp.Queue()
    process = mp.Process(target=fetch_worker, args=(queue,))
    process.start()
    process.join(seconds)

    if process.is_alive():
        process.terminate()
        process.join(5)
        raise FetchTimeoutError(f"Timed out after {seconds}s")

    if queue.empty():
        raise RuntimeError("Scholar fetch exited without returning data")

    status, payload = queue.get()
    if status == "ok":
        return payload
    raise RuntimeError(payload)


def prepare_author(author):
    author["updated"] = str(datetime.now())
    author.pop("fallback_updated", None)
    author.pop("fallback_reason", None)

    pubs = {}
    for publication in author.get("publications", []):
        bib = publication.get("bib", {})
        author_pub_id = publication.get("author_pub_id")
        if author_pub_id:
            pubs[author_pub_id] = publication

        title = norm_title(bib.get("title", ""))
        if title:
            pubs[title] = publication

    author["publications"] = pubs
    return author


def write_results(author):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    with open(os.path.join(RESULTS_DIR, GS_DATA), "w", encoding="utf-8") as outfile:
        json.dump(author, outfile, ensure_ascii=False)

    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": f"{author.get('citedby', 0)}",
    }
    with open(os.path.join(RESULTS_DIR, SHIELDS_DATA), "w", encoding="utf-8") as outfile:
        json.dump(shieldio_data, outfile, ensure_ascii=False)


def download_json(url, timeout=20):
    with urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def write_fallback_results():
    repository = os.environ.get("GITHUB_REPOSITORY", "Andysis/andysis.github.io")
    base_url = f"https://raw.githubusercontent.com/{repository}/google-scholar-stats"
    gs_url = f"{base_url}/{GS_DATA}"
    shields_url = f"{base_url}/{SHIELDS_DATA}"

    print("Trying to reuse the latest published citation data...")
    author = download_json(gs_url)
    author["fallback_updated"] = str(datetime.now())
    author["fallback_reason"] = "Google Scholar fetch failed; reused latest published data."

    try:
        shieldio_data = download_json(shields_url)
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Could not fetch shield data, rebuilding it locally: {exc}")
        shieldio_data = {
            "schemaVersion": 1,
            "label": "citations",
            "message": f"{author.get('citedby', 0)}",
        }

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, GS_DATA), "w", encoding="utf-8") as outfile:
        json.dump(author, outfile, ensure_ascii=False)
    with open(os.path.join(RESULTS_DIR, SHIELDS_DATA), "w", encoding="utf-8") as outfile:
        json.dump(shieldio_data, outfile, ensure_ascii=False)

    print(
        json.dumps(
            {
                "fallback": True,
                "name": author.get("name"),
                "citedby": author.get("citedby"),
                "pub_count": len(author.get("publications", {})),
            },
            indent=2,
        )
    )


def main():
    print(f"Fetching the public Scholar profile ({DIRECT_TIMEOUT}s timeout)...")

    try:
        author = prepare_author(fetch_profile_direct())
        write_results(author)
        print(
            json.dumps(
                {
                    "name": author.get("name"),
                    "citedby": author.get("citedby"),
                    "pub_count": len(author.get("publications", {})),
                    "source": author.get("data_source"),
                },
                indent=2,
            )
        )
        print("Done.")
        return
    except Exception as exc:
        print(f"Direct profile fetch failed: {exc}")

    print(
        "Trying the scholarly fallback "
        f"({MAX_ATTEMPTS} attempt(s), {FETCH_TIMEOUT}s timeout each)..."
    )

    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            author = prepare_author(fetch_with_timeout(FETCH_TIMEOUT))
            write_results(author)
            print(
                json.dumps(
                    {
                        "name": author.get("name"),
                        "citedby": author.get("citedby"),
                        "pub_count": len(author.get("publications", {})),
                        "source": author.get("data_source"),
                    },
                    indent=2,
                )
            )
            print("Done.")
            return
        except Exception as exc:
            last_error = exc
            print(f"Attempt {attempt} failed: {exc}")
            if attempt < MAX_ATTEMPTS:
                wait = attempt * RETRY_BASE_SECONDS
                print(f"Retrying in {wait}s...")
                time.sleep(wait)

    print(f"All Scholar attempts failed: {last_error}")
    try:
        write_fallback_results()
        print("Done with fallback data.")
    except Exception as fallback_error:
        raise RuntimeError(
            f"Scholar fetch failed and fallback data could not be reused: {fallback_error}"
        ) from fallback_error


if __name__ == "__main__":
    main()
