from scholarly import scholarly
import json
from datetime import datetime
import os
import time
import signal

class TimeoutError(Exception):
    pass

def with_timeout(seconds):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError(f"Timed out after {seconds}s")
        def wrapper(*args, **kwargs):
            old = signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old)
        return wrapper
    return decorator

def norm_title(s):
    return s.lower().replace('\n', ' ').replace('\r', ' ').strip()

def try_fetch():
    author = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
    return author

print("Fetching from Google Scholar (direct connection)...")

attempts = 0
FETCH_TIMEOUT = 120
while attempts < 3:
    try:
        author = with_timeout(FETCH_TIMEOUT)(try_fetch)()
        break
    except (TimeoutError, Exception) as e:
        attempts += 1
        print(f"Attempt {attempts} failed: {e}")
        if attempts < 3:
            wait = attempts * 30
            print(f"Retrying in {wait}s...")
            time.sleep(wait)
else:
    raise RuntimeError("All attempts failed")

name = author['name']
author['updated'] = str(datetime.now())

pubs = {}
for v in author['publications']:
    bib = v.get('bib', {})
    pubs[v['author_pub_id']] = v
    title = norm_title(bib.get('title', ''))
    pubs[title] = v

author['publications'] = pubs

print(json.dumps({'name': author.get('name'), 'citedby': author.get('citedby'), 'pub_count': len(author.get('publications', {}))}, indent=2))

os.makedirs('results', exist_ok=True)
with open('results/gs_data.json', 'w', encoding='utf-8') as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": f"{author.get('citedby', 0)}",
}
with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)

print("Done.")
