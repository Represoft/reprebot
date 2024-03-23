from typing import List
import requests
from bs4 import BeautifulSoup
import hashlib

def get_html(url: str):
    response = requests.get(url)
    return response.text


def write_file(text: str) -> None:
    md5_hash = hashlib.md5(text.encode()).hexdigest()
    with open(f"{md5_hash}.txt", "w", encoding="utf-8") as file:
        file.write(text)


def assemble_text(button):
    button_text = button.get_text(strip=True)
    next_div = button.find_next_sibling('div')
    if next_div:
        div_text = next_div.get_text(strip=True)
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


def main():
    url = "https://ingenieria.bogota.unal.edu.co/es/dependencias/secretaria-academica/preguntas-frecuentes.html"
    html = get_html(url)
    texts = extract_texts(html)
    list(map(write_file, texts))


if __name__ == "__main__":
    main()
