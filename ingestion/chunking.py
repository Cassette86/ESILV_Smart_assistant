"""
ETAPE 2 - GENERATION DES CHUNKS POUR LE RAG
-------------------------------------------

Ce script constitue la deuxième partie de l’étape d’ingestion des données
pour le projet ESILV Smart Assistant.

Après avoir extrait et nettoyé les fichiers PDF (extract_text.py),
nous devons maintenant découper les textes en "chunks" (morceaux)
afin de préparer l’indexation vectorielle du système RAG.

Pourquoi faire du chunking ?
----------------------------
Les modèles d’IA et les vector stores ne fonctionnent pas sur de grands blocs
de texte. Ils utilisent des embeddings (représentations numériques) qui ont 
une taille maximale. Pour permettre :

- une recherche pertinente,
- un contexte bien structuré,
- une réponse précise aux questions,

il faut découper les documents en segments de taille raisonnable (ex : 500 tokens),
avec un léger overlap pour ne pas couper le sens.

Ce script :
-----------
- Parcourt les fichiers .txt du dossier data/processed/.
- Convertit le texte en tokens.
- Découpe le texte en chunks de longueur CHUNK_SIZE avec overlap.
- Génère un fichier chunks.jsonl contenant :
      { "source": "nom_du_document", "chunk": "contenu_du_chunk" }

Résultat :
----------
Le fichier chunks.jsonl est prêt à être utilisé pour construire l’index vectoriel
(étape suivante : build_index.py). C’est une étape essentielle au fonctionnement
du chatbot, car elle permet au modèle de retrouver efficacement l’information 
dans les documents officiels de l’ESILV.
"""



import os
import json
import tiktoken

PROCESSED_DIR = "data/processed"
OUTPUT_FILE = "data/chunks.jsonl"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def tokenize(text):
    enc = tiktoken.get_encoding("cl100k_base")
    return enc.encode(text)

def detokenize(tokens):
    enc = tiktoken.get_encoding("cl100k_base")
    return enc.decode(tokens)

def create_chunks(text, source):
    tokens = tokenize(text)
    chunks = []

    start = 0
    end = CHUNK_SIZE

    while start < len(tokens):
        chunk_tokens = tokens[start:end]
        chunk_text = detokenize(chunk_tokens)

        chunks.append({
            "source": source,
            "chunk": chunk_text
        })

        start += CHUNK_SIZE - CHUNK_OVERLAP
        end = start + CHUNK_SIZE

    return chunks

def build_chunks():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for filename in os.listdir(PROCESSED_DIR):
            if filename.endswith(".txt"):
                print(f"[INFO] Chunking {filename}...")

                filepath = os.path.join(PROCESSED_DIR, filename)

                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()

                chunks = create_chunks(text, filename)

                for c in chunks:
                    out.write(json.dumps(c) + "\n")

                print(f"[OK] {filename} done.")

if __name__ == "__main__":
    build_chunks()