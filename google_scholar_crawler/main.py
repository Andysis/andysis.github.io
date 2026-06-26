from datetime import datetime
import json
import multiprocessing as mp
import os
import time
from urllib.error import URLError
from urllib.request import urlopen

from scholarly import scholarly


RESULTS_DIR = "results"
GS_DATA = "gs_data.json"
SHIELDS_DATA = "gs_data_shieldsio.json"
FETCH_TIMEOUT = int(os.environ.get("SCHOLAR_FETCH_TIMEOUT", "75"))
MAX_ATTEMPTS = int(os.environ.get("SCHOLAR_MAX_ATTEMPTS", "2"))
RETRY_BASE_SECONDS = int(os.environ.get("SCHOLAR_RETRY_BASE_SECONDS", "15"))


class FetchTimeoutError(Exception):
    pass


def norm_title(s):
    return s.lower().replace("\n", " ").replace("\r", " ").strip()


def fetch_author():
    author = scholarly.search_author_id(os.environ["GOOGLE_SCHOLAR_ID"])
    scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])
    return author


def fetch_worker(queue):
    try:
        queue.put(("ok", fetch_author()))
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
    print(
        "Fetching from Google Scholar "
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
