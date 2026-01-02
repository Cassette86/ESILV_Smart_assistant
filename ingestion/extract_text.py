"""
ETAPE 1 - EXTRACTION ET NETTOYAGE DES DOCUMENTS ESILV
-----------------------------------------------------

Ce script fait partie de la phase d’ingestion du projet ESILV Smart Assistant.
L’objectif est de transformer toutes les sources PDF (plaquettes, livrets, chartes…)
en fichiers texte exploitables pour la construction du RAG (Retrieval-Augmented Generation).

Pourquoi cette étape ?
----------------------
Les modèles d’IA ne peuvent pas lire directement des fichiers PDF. 
Pour pouvoir analyser et indexer le contenu dans un vector store, il faut :
1. Extraire le texte brut depuis chaque PDF.
2. Nettoyer ce texte (espaces, sauts de ligne inutiles…).
3. Sauvegarder un fichier .txt par document dans data/processed/.

Ce script :
-----------
- Parcourt automatiquement tous les PDF du dossier data/raw/.
- Extrait le texte avec la librairie pypdf.
- Nettoie le texte avec une fonction clean_text().
- Sauvegarde le texte propre dans data/processed/.

Résultat :
----------
Les fichiers .txt produits serviront ensuite à créer des chunks 
(étape suivante : chunking.py) qui seront indexés dans une base vectorielle
pour permettre au chatbot de répondre à partir des documents officiels ESILV.
"""


import os
from pypdf import PdfReader

RAW_DIR = "data/raw"
WEB_DIR = "data/raw/web"
PDF_DIR = "data/raw/brochures"
PROCESSED_DIR = "data/processed"

NAVIGATION_KEYWORDS = [
    "menu",
    "admissions",
    "presse",
    "agenda",
    "close",
    "journées portes ouvertes",
    "vie étudiante",
    "formations",
    "candidature",
    "pratique",
    "accès",
    "campus"
]

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def clean_text(text):
    cleaned_lines = []

    for line in text.split("\n"):
        line = line.strip()

        # skip empty
        if not line:
            continue

        # skip navigation/menu lines
        if any(keyword in line.lower() for keyword in NAVIGATION_KEYWORDS):
            continue

        # skip very short lines (menu items, noise)
        if len(line) < 40:
            continue

        cleaned_lines.append(line)

    # 🔽 DÉDUPLICATION : À FAIRE ICI, EN DEHORS DE LA BOUCLE
    seen = set()
    unique_lines = []
    for line in cleaned_lines:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)

    return "\n".join(unique_lines)


def save_text_file(filename, content):
    output_path = os.path.join(PROCESSED_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

def process_pdfs():
    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, filename)
            print(f"[INFO] Extracting PDF {filename}...")

            raw_text = extract_text_from_pdf(pdf_path)
            text = clean_text(raw_text)

            save_text_file(filename.replace(".pdf", ".txt"), text)
            print(f"[OK] Saved PDF -> {filename.replace('.pdf', '.txt')}")

def process_web_pages():
    for filename in os.listdir(WEB_DIR):
        if filename.endswith(".txt"):
            txt_path = os.path.join(WEB_DIR, filename)
            print(f"[INFO] Processing web page {filename}...")

            with open(txt_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            text = clean_text(raw_text)
            save_text_file(filename, text)

            print(f"[OK] Saved WEB -> {filename}")

def extract_all_texts():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    #process_pdfs()
    process_web_pages()

    print("[DONE] All documents processed successfully.")

if __name__ == "__main__":
    extract_all_texts()