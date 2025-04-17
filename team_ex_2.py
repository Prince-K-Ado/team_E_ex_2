import time
import wikipedia
import os
import re
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# --- Helper Functions ---

def convert_to_str(obj):
    """Convert object (list, str, int, float) to a string."""
    if isinstance(obj, list):
        return '\n'.join(obj)
    return str(obj)

def safe_filename(name):
    """Sanitize a string to be safe as a filename."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def ensure_directory(path="wiki_dl"):
    """Ensure that the target directory exists."""
    os.makedirs(path, exist_ok=True)

def download_and_save(item):
    """Download references from a Wikipedia page and save them to a text file."""
    try:
        page = wikipedia.page(item, auto_suggest=False)
        title = safe_filename(page.title)
        references = convert_to_str(page.references)
        file_path = os.path.join("wiki_dl", title + ".txt")
        print(f'writing to {file_path}')
        with open(file_path, 'w', encoding='utf-8') as fileobj:
            fileobj.write(references)
    except Exception as e:
        print(f"Error processing '{item}': {e}")

# --- Execution Modes ---

def run_sequential(results):
    print("\nRunning sequential...")
    start = time.perf_counter()
    for item in results:
        download_and_save(item)
    print(f"Done in {time.perf_counter() - start:.2f}s")

def run_threads(results):
    print("\nRunning with ThreadPoolExecutor...")
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_and_save, results)
    print(f"Done in {time.perf_counter() - start:.2f}s")

def run_processes(results):
    print("\nRunning with ProcessPoolExecutor...")
    start = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        executor.map(download_and_save, results)
    print(f"Done in {time.perf_counter() - start:.2f}s")

# --- Main Execution Block ---

if __name__ == "__main__":
    ensure_directory()

    user_input = input("Enter a Wikipedia search term: ").strip()
    if len(user_input) < 4:
        print("Input too short, defaulting to 'generative artificial intelligence'.")
        user_input = "generative artificial intelligence"

    print(f"Searching Wikipedia for '{user_input}'...")
    results = wikipedia.search(user_input)

    if not results:
        print("No results found.")
    else:
        run_sequential(results)
        run_threads(results)
        run_processes(results)