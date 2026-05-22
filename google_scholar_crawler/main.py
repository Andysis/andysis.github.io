from scholarly import scholarly, ProxyGenerator
import json
from datetime import datetime
import os
import time

def norm_title(s):
    return s.lower().replace('\n', ' ').replace('\r', ' ').strip()

def try_fetch():
    author = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
    return author

pg = ProxyGenerator()
proxy_ok = False
try:
    proxy_ok = pg.FreeProxies()
except Exception:
    pass

if proxy_ok:
    scholarly.use_proxy(pg)
    print("Using FreeProxies")

attempts = 0
while attempts < 3:
    try:
        author = try_fetch()
        break
    except Exception as e:
        attempts += 1
        print(f"Attempt {attempts} failed: {e}")
        if attempts < 3:
            wait = attempts * 30
            print(f"Retrying in {wait}s...")
            time.sleep(wait)
else:
    if proxy_ok:
        print("Proxy failed, trying direct connection...")
        scholarly.use_proxy(None)
        author = try_fetch()
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
