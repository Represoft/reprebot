from typing import List
import requests
from bs4 import BeautifulSoup
from cryptography.hazmat.primitives import hashes
import os
import sys
sys.path.append('../../..')
from src.constants import PROJECT_ROOT

def get_html(url: str):
    response = requests.get(url, timeout=5)
    return response.text


def setup_folder(folder: str = os.path.join(PROJECT_ROOT, 'data/faculty_secretary_faq')) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)


def write_file(text: str, folder: str = os.path.join(PROJECT_ROOT, 'data/faculty_secretary_faq')) -> None:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(text.encode())
    file_name = digest.finalize().hex()
    with open(f"{folder}/{file_name}.txt", "w", encoding="utf-8") as file:
        file.write(text)


def assemble_text(button):
    button_text = button.get_text()
    next_div = button.find_next_sibling('div')
    if next_div:
        div_text = next_div.get_text()
        anchors = next_div.find_all('a')
        href_values = [anchor['href'] for anchor in anchors]
        combined_text = div_text + "\n" + "\n".join(href_values)
        text = f"{button_text}\n{combined_text}\n"
        return text


def extract_texts(html) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    buttons = soup.find_all('button', class_='accordion')
    texts = list(map(assemble_text, buttons))
    return texts


def main(): # pragma: no cover
    # functions are already tested
    url = "https://ingenieria.bogota.unal.edu.co/es/dependencias/secretaria-academica/preguntas-frecuentes.html"
    html = get_html(url)
    texts = extract_texts(html)
    setup_folder()
    list(map(write_file, texts))


if __name__ == "__main__": # pragma: no cover
    # functions are already tested
    main()
