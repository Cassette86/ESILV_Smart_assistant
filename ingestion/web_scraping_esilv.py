import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

def scrape_esilv_website():


    start_url = "https://www.esilv.fr/"
    output_dir = "data/raw/web/"
    os.makedirs(output_dir, exist_ok=True)

    visited = set()
    to_visit = [start_url]

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)
    
        try:
            response = requests.get(url)
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.text, "html.parser")
        
            # Nettoyer texte
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator="\n")
            text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
        
            # Nom de fichier basé sur URL
            filename = urlparse(url).path.replace("/", "_").strip("_") or "home"
            with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
                f.write(text)
        
            # Trouver toutes les liens internes
            for a_tag in soup.find_all("a", href=True):
                link = urljoin(start_url, a_tag['href'])
            
                # ❌ Ignorer les liens vers /download/
                if link.startswith("https://www.esilv.fr/download/"):
                    continue
            
                # Ajouter seulement les liens internes
                if urlparse(link).netloc == urlparse(start_url).netloc:
                    if link not in visited and link not in to_visit:
                        to_visit.append(link)
                    
            print(f"[OK] {url}")
        except Exception as e:
            print(f"[Erreur] {url} -> {e}")
