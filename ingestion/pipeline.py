from scraping import scrape_esilv_website
from extract_text import extract_all_texts
from chunking import build_chunks, load_chunks
from build_index import build_or_update_index

def run_pipeline():
    print("=== STEP 1: Scraping ===")
    scrape_esilv_website()

    print("=== STEP 2: Text extraction ===")
    extract_all_texts()

    print("=== STEP 3: Chunking ===")
    build_chunks()

    print("=== STEP 4: Indexing ===")
    chunks = load_chunks("data/chunks.jsonl")
    build_or_update_index(chunks)

    print("=== PIPELINE DONE ===")

if __name__ == "__main__":
    run_pipeline()