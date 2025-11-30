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
PROCESSED_DIR = "data/processed"

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def clean_text(text):
    text = text.replace("\t", " ")
    text = text.replace("  ", " ")
    lines = [line.strip() for line in text.split("\n") if line.strip() != ""]
    return "\n".join(lines)


def save_text_file(filename, content):
    output_path = os.path.join(PROCESSED_DIR, filename.replace(".pdf", ".txt"))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    for filename in os.listdir(RAW_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(RAW_DIR, filename)
            print(f"[INFO] Extracting {filename}...")

            #text = extract_text_from_pdf(pdf_path)
            text = clean_text(extract_text_from_pdf(pdf_path))

            save_text_file(filename, text)

            print(f"[OK] Saved: {filename.replace('.pdf', '.txt')}")

if __name__ == "__main__":
    main()
