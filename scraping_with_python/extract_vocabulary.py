import csv
import time
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ============ CONFIG ===============
load_dotenv()

# Read variables
DEBUGGER_ADDRESS = os.getenv("DEBUGGER_ADDRESS")
INPUT_LINKS_CSV = os.getenv("INPUT_LINKS_CSV")
OUTPUT_WORDS_CSV = os.getenv("OUTPUT_WORDS_CSV")
# ===================================

options = Options()
options.add_experimental_option("debuggerAddress", DEBUGGER_ADDRESS)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 12)


# -------------------------
# Cargar CSV con los links
# -------------------------
def load_links():
    links = []
    with open(INPUT_LINKS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            links.append(row["vocab_link"])
    return links


# -------------------------
# Guardar resultados append
# -------------------------
def append_words(rows):
    write_header = False
    try:
        open(OUTPUT_WORDS_CSV, "r", encoding="utf-8").close()
    except FileNotFoundError:
        write_header = True

    with open(OUTPUT_WORDS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["url", "index", "word", "category", "definition", "example"]
        )
        if write_header:
            writer.writeheader()
        for r in rows:
            writer.writerow(r)


# -------------------------
# EXTRAER INFO DE UNA TARJETA
# -------------------------
def extract_card_info():
    # word
    try:
        word = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".c-cbaGBs"))
        ).text.strip()
    except:
        word = ""

    # category
    try:
        category = driver.find_element(By.CSS_SELECTOR, ".c-bdLXHL").text.strip()
    except:
        category = ""

    # definition
    try:
        definition = driver.find_element(By.CSS_SELECTOR, "div.c-kvHruh").text.strip()
    except:
        definition = ""

    # examples (pueden ser varios)
    # examples (pueden ser varios). Buscamos dentro del wrapper principal y también p.c-cDXIIJ
    example_texts = []

    # 1) Piezas explícitas con la clase (p.c-cDXIIJ)
    try:
        elems1 = driver.find_elements(By.CSS_SELECTOR, "p.c-cDXIIJ")
        for e in elems1:
            txt = e.text.strip()
            if txt:
                example_texts.append(txt)
    except:
        pass

    # 2) P dentro del wrapper div.c-jHvPkb que tenga dir="auto" (captura el caso mostrado)
    try:
        elems2 = driver.find_elements(By.CSS_SELECTOR, "div.c-jHvPkb p[dir='auto']")
        for e in elems2:
            txt = e.text.strip()
            if txt and txt not in example_texts:
                example_texts.append(txt)
    except:
        pass

    # 3) Fallback: cualquier p[dir='auto'] cercano (evitar duplicados)
    if not example_texts:
        try:
            elems3 = driver.find_elements(By.CSS_SELECTOR, "p[dir='auto']")
            for e in elems3:
                txt = e.text.strip()
                # filtrar cosas cortas o títulos (por si)
                if txt and len(txt) > 10 and txt not in example_texts:
                    example_texts.append(txt)
        except:
            pass

    example = "\n".join(
        example_texts
    ).strip()  # examples (pueden ser varios). Buscamos dentro del wrapper principal y también p.c-cDXIIJ
    example_texts = []

    # 1) Piezas explícitas con la clase (p.c-cDXIIJ)
    try:
        elems1 = driver.find_elements(By.CSS_SELECTOR, "p.c-cDXIIJ")
        for e in elems1:
            txt = e.text.strip()
            if txt:
                example_texts.append(txt)
    except:
        pass

    # 2) P dentro del wrapper div.c-jHvPkb que tenga dir="auto" (captura el caso mostrado)
    try:
        elems2 = driver.find_elements(By.CSS_SELECTOR, "div.c-jHvPkb p[dir='auto']")
        for e in elems2:
            txt = e.text.strip()
            if txt and txt not in example_texts:
                example_texts.append(txt)
    except:
        pass

    # 3) Fallback: cualquier p[dir='auto'] cercano (evitar duplicados)
    if not example_texts:
        try:
            elems3 = driver.find_elements(By.CSS_SELECTOR, "p[dir='auto']")
            for e in elems3:
                txt = e.text.strip()
                # filtrar cosas cortas o títulos (por si)
                if txt and len(txt) > 10 and txt not in example_texts:
                    example_texts.append(txt)
        except:
            pass

    example = "\n".join(example_texts).strip()

    return word, category, definition, example


# -------------------------
# PROCESAR UN LINK
# -------------------------
def process_link(url, index):
    driver.get(url)
    time.sleep(3)

    results = []
    tarjeta = 1

    while True:
        try:
            word, cat, defi, ex = extract_card_info()

            if not word:
                print("❌ No se encontró palabra. Fin.")
                break

            results.append(
                {
                    "url": url,
                    "index": tarjeta,
                    "word": word,
                    "category": cat,
                    "definition": defi,
                    "example": ex,
                }
            )

            print(f"[{tarjeta}] {word}")
            if ex:
                print(f"    example -> {ex.splitlines()[0][:120]}")

            # Click botón "Continuar"
            clicked = False
            # probamos la clase que me diste (.c-jUtMbh) y la otra (.c-lfgsZH) como fallback
            for sel in ("button.c-jUtMbh", "button.c-lfgsZH", "button.c-lfgsZH.c-PJLV"):
                try:
                    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1)
                    tarjeta += 1
                    clicked = True
                    break
                except:
                    continue

            if not clicked:
                # no hay más continuar
                print("✔ No hay más 'Continuar'.")
                break

        except Exception as e:
            print("Error:", e)
            break

    append_words(results)
    print(f"Guardadas {len(results)} palabras.\n")


# -------------------------
# MENU PRINCIPAL
# -------------------------
def main():
    links = load_links()
    print(f"Links cargados: {len(links)}")

    while True:
        idx = input("Ingresa el índice a procesar (o 'q' para salir): ")

        if idx.lower() == "q":
            break

        if not idx.isdigit() or int(idx) >= len(links):
            print("Índice inválido.\n")
            continue

        idx = int(idx)
        url = links[idx]
        print(f"\n=== Procesando índice {idx} ===")
        print(f"URL: {url}")
        process_link(url, idx)

    print("Terminado.")


if __name__ == "__main__":
    main()


# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeSelenium"
