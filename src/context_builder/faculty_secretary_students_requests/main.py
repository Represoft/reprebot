from typing import List
import requests
from bs4 import BeautifulSoup
from cryptography.hazmat.primitives import hashes
import os
import sys

sys.path.append("../../..")
from src.constants import CONTEXT_DATA_PATHS, CONTEXT_DATA_SOURCES
import re


FOLDER = CONTEXT_DATA_PATHS["faculty_secretary_students_requests"]
URL = CONTEXT_DATA_SOURCES["faculty_secretary_students_requests"]


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


def extract_texts(html) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.find_all("h3", class_="subtitle_content")
    texts = []
    for section in sections:
        section_text = format_text(section.get_text())
        sibling = section.find_next_sibling("ul", class_="list_enumerate")
        if sibling:
            items = sibling.find_all("li")
            for item in items:
                item_text = format_text(item.get_text())
                text = f"{section_text}: {item_text}"
                texts.append(text)
    return texts


def main():  # pragma: no cover
    # functions are already tested
    html = get_html(URL)
    texts = extract_texts(html)
    setup_folder()
    list(map(write_file, texts))


if __name__ == "__main__":  # pragma: no cover
    # functions are already tested
    main()
