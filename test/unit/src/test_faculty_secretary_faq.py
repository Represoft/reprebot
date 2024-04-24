import os
from cryptography.hazmat.primitives import hashes
from typing import List
from bs4 import BeautifulSoup
import pytest
from src.context_builder.faculty_secretary_faq.main import (
    get_html,
    setup_folder,
    write_file,
    assemble_text,
    extract_texts,
)
import shutil
from src.constants import PROJECT_ROOT


MOCK_HTML = """
<html>
    <body>
        <button class="accordion">Button 1</button>
        <div>Content 1 <a href="link1">Link 1</a></div>
        <button class="accordion">Button 2</button>
        <div>Content 2 <a href="link2">Link 2</a></div>
    </body>
</html>
"""


@pytest.mark.parametrize(
    ("url"),
    [
        ("https://example.com/"),
        ("https://google.com"),
    ],
)
def test_get_html(url: str):
    html = get_html(url=url)
    assert html is not None


@pytest.mark.parametrize(
    ("folder"),
    [
        (os.path.join(PROJECT_ROOT, "test/test-data/faculty_secretary_faq")),
    ],
)
def test_setup_folder(folder: str):
    setup_folder(folder=folder)
    assert os.path.exists(folder)
    shutil.rmtree(folder)


@pytest.mark.parametrize(
    ("folder", "text"),
    [
        (
            os.path.join(PROJECT_ROOT, "test/test-data/faculty_secretary_faq"),
            "Test content",
        ),
    ],
)
def test_write_file(folder: str, text: str):
    setup_folder(folder=folder)
    write_file(text=text, folder=folder)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(text.encode())
    file_name = digest.finalize().hex()
    file_path = f"{folder}/{file_name}.txt"
    assert os.path.exists(file_path)
    shutil.rmtree(folder)


@pytest.mark.parametrize(
    ("_text"),
    [
        ("Button 1\n\nContent 1 Link 1\n\nENLACES:\n[Link 1](link1)\n"),
    ],
)
def test_assemble_text(_text: str):
    button = BeautifulSoup(MOCK_HTML, "html.parser").find("button")
    text = assemble_text(button=button)
    assert text == _text


@pytest.mark.parametrize(
    ("_texts"),
    [
        (
            [
                "Button 1\n\nContent 1 Link 1\n\nENLACES:\n[Link 1](link1)\n",
                "Button 2\n\nContent 2 Link 2\n\nENLACES:\n[Link 2](link2)\n",
            ]
        ),
    ],
)
def test_extract_texts(_texts: List[str]):
    texts = extract_texts(html=MOCK_HTML)
    assert texts == _texts
