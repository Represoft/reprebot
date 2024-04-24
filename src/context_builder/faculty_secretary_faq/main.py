from typing import List
import requests
from bs4 import BeautifulSoup
from cryptography.hazmat.primitives import hashes
import os
import sys

sys.path.append("../../..")
from src.constants import CONTEXT_DATA_PATHS
import re


FOLDER = CONTEXT_DATA_PATHS["faculty_secretary_faq"]


def get_html(url: str):
    response = requests.get(url, timeout=5)
    return response.text


def setup_folder(folder: str = FOLDER) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)


def write_file(text: str, folder: str = FOLDER) -> None:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(text.encode())
    file_name = digest.finalize().hex()
    with open(f"{folder}/{file_name}.txt", "w", encoding="utf-8") as file:
        file.write(text)


def format_text(text: str) -> str:
    formatted_text = re.sub(r"\s+", " ", text).strip()
    return formatted_text


def assemble_text(button):
    button_text = format_text(button.get_text())
    next_div = button.find_next_sibling("div")
    if next_div:
        div_text = format_text(next_div.get_text())
        anchors = next_div.find_all("a")
        href_text = "\n".join(
            [
                f"[{format_text(anchor.get_text())}]({anchor['href']})"
                for anchor in anchors
            ]
        )
        href_text = (
            "\n\nENLACES:\n" + href_text if len(href_text) > 0 else href_text
        )
        combined_text = f"{div_text}{href_text}"
        text = f"{button_text}\n\n{combined_text}\n"
        return text


def extract_texts(html) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    buttons = soup.find_all("button", class_="accordion")
    texts = list(map(assemble_text, buttons))
    return texts


def main():  # pragma: no cover
    # functions are already tested
    url = "https://ingenieria.bogota.unal.edu.co/es/dependencias/secretaria-academica/preguntas-frecuentes.html"
    html = get_html(url)
    texts = extract_texts(html)
    setup_folder()
    list(map(write_file, texts))


if __name__ == "__main__":  # pragma: no cover
    # functions are already tested
    main()
