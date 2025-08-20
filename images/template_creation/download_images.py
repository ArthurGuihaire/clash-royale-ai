#!/usr/bin/env python3
import os
import time
import math
import concurrent.futures as cf
from typing import List, Optional
import requests
from urllib.parse import urlparse, unquote, quote

API_URL = "https://clashroyale.fandom.com/api.php"
DEST_DIR = "templates"
MAX_WORKERS = 12
TIMEOUT = 30
RETRIES = 4
BACKOFF_BASE = 0.75  # seconds

os.makedirs(DEST_DIR, exist_ok=True)

session = requests.Session()
session.headers.update({
    "User-Agent": "CR-ImageDownloader/1.0 (youremail@example.com)",
    "Accept": "*/*",
})

# ------------------------
# Helpers
# ------------------------
def nice_name_from_url(url: str) -> str:
    """Return a descriptive PNG filename from a Fandom image URL."""
    p = urlparse(url)
    parts = [s for s in p.path.split('/') if s]

    for seg in reversed(parts):
        if seg.lower().endswith('.png'):
            return unquote(seg)

    if 'revision' in parts:
        i = parts.index('revision')
        if i > 0:
            return unquote(parts[i - 1])

    return unquote(os.path.basename(p.path)) or "image.png"


def filepage_name_to_filename(title: str) -> str:
    # "File:ArchersCard.png" -> "ArchersCard.png"
    return title.split(':', 1)[1] if ':' in title else title


def direct_file_url(filename: str) -> str:
    # This redirects to the actual binary on static.wikia.nocookie.net
    # Adding redirect=yes keeps behavior explicit.
    return f"https://clashroyale.fandom.com/wiki/Special:FilePath/{quote(filename)}?redirect=yes"


def fetch_image_pages(cmcontinue: Optional[str] = None) -> dict:
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': 'Category:Card Images',
        'cmtype': 'file',
        'cmlimit': 'max',
        'format': 'json',
    }
    if cmcontinue:
        params['cmcontinue'] = cmcontinue
    resp = session.get(API_URL, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def collect_png_titles() -> List[str]:
    print("Fetching list of image files in category...")
    cmcontinue = None
    all_titles: List[str] = []
    while True:
        data = fetch_image_pages(cmcontinue)
        members = data.get('query', {}).get('categorymembers', [])
        for m in members:
            title = m.get('title', '')
            if title.lower().endswith('.png'):
                all_titles.append(title)
        cont = data.get('continue', {}).get('cmcontinue')
        if cont:
            cmcontinue = cont
        else:
            break
    return all_titles


def save_response_to_file(resp: requests.Response, local_path: str) -> None:
    with open(local_path, "wb") as f:
        for chunk in resp.iter_content(8192):
            if chunk:
                f.write(chunk)


def is_image_response(resp: requests.Response) -> bool:
    ctype = (resp.headers.get("Content-Type") or "").lower()
    return ctype.startswith("image/")


def download_one(filename: str) -> str:
    """
    Download a single file by filename (e.g., ArchersCard.png) using Special:FilePath.
    Retries with exponential backoff on transient errors and non-image responses.
    Returns the saved local path (or a message).
    """
    url = direct_file_url(filename)
    target_name = nice_name_from_url(url)
    local_path = os.path.join(DEST_DIR, target_name)

    last_err = None
    for attempt in range(1, RETRIES + 1):
        try:
            r = session.get(
                url,
                stream=True,
                timeout=TIMEOUT,
                allow_redirects=True,
                headers={
                    # some CDNs block direct hotlinks; provide a referer
                    "Referer": "https://clashroyale.fandom.com/",
                },
            )
            # Handle common transient statuses
            if r.status_code in (429, 500, 502, 503, 504):
                last_err = RuntimeError(f"HTTP {r.status_code}")
                raise last_err
            r.raise_for_status()

            if not is_image_response(r):
                # HTML viewer or block page — backoff and retry
                text_sample = r.text[:120].replace("\n", " ")
                last_err = RuntimeError(f"Not an image (Content-Type={r.headers.get('Content-Type')!r}, sample={text_sample!r})")
                raise last_err

            save_response_to_file(r, local_path)
            return f"OK {filename} -> {local_path}"
        except Exception as e:
            last_err = e
            # backoff
            if attempt < RETRIES:
                sleep_s = BACKOFF_BASE * (2 ** (attempt - 1)) * (1 + 0.1 * attempt)
                time.sleep(sleep_s)
            else:
                break

    return f"FAIL {filename}: {last_err}"


def main():
    titles = collect_png_titles()
    print(f"Found {len(titles)} PNG images. Downloading via Special:FilePath...")

    filenames = [filepage_name_to_filename(t) for t in titles]

    # Parallel downloads
    successes = 0
    failures = 0
    with cf.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(download_one, fn) for fn in filenames]
        for i, fut in enumerate(cf.as_completed(futures), 1):
            msg = fut.result()
            if msg.startswith("OK"):
                successes += 1
            else:
                failures += 1
            print(f"[{i:>3}/{len(filenames)}] {msg}")

    print(f"All done! Success: {successes}, Failures: {failures}")


if __name__ == "__main__":
    main()
