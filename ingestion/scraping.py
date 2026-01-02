import json
import hashlib
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import hashlib

METADATA_PATH = "data/metadata/pages.json"

def load_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

def compute_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def scrape_esilv_website():
    start_url = "https://www.esilv.fr/"
    output_dir = "data/raw/web/"
    os.makedirs(output_dir, exist_ok=True)

    metadata = load_metadata()

    visited = set()
    to_visit = [start_url]

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        # Ignorer les pages en anglais
        if "/en/" in urlparse(url).path:
            continue

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # Nettoyage HTML
            for tag in soup(["script", "style"]):
                tag.decompose()

            text = soup.get_text(separator="\n")
            text = "\n".join(
                line.strip() for line in text.splitlines() if line.strip()
            )

            content_hash = compute_hash(text)

            # Nom de fichier stable
            path_part = urlparse(url).path.replace("/", "_").strip("_") or "home"
            if len(path_part) > 50:
                path_part = path_part[:50] + "_" + hashlib.md5(path_part.encode()).hexdigest()[:6]
            filename = f"{path_part}.txt"
            filepath = os.path.join(output_dir, filename)

            # ----------- LOGIQUE INCRÉMENTALE -----------
            if url in metadata:
                if metadata[url]["hash"] == content_hash:
                    print(f"[SKIP] {url} (unchanged)")
                else:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(text)
                    metadata[url]["hash"] = content_hash
                    metadata[url]["last_scraped"] = datetime.now().isoformat()
                    print(f"[UPDATE] {url}")
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)
                metadata[url] = {
                    "filename": filename,
                    "hash": content_hash,
                    "last_scraped": datetime.now().isoformat()
                }
                print(f"[NEW] {url}")

            # ----------- DÉCOUVERTE DES LIENS -----------
            for a in soup.find_all("a", href=True):
                link = urljoin(start_url, a["href"])

                if link.startswith("https://www.esilv.fr/download/"):
                    continue
                if "/en/" in urlparse(link).path:
                    continue
                if urlparse(link).netloc == urlparse(start_url).netloc:
                    if link not in visited and link not in to_visit:
                        to_visit.append(link)

        except Exception as e:
            print(f"[ERROR] {url} -> {e}")

    save_metadata(metadata)


if __name__ == "__main__":
    scrape_esilv_website()