import os
import hashlib
from bs4 import BeautifulSoup
from src.context_builder.faculty_secretary_faq.main import (
    get_html,
    setup_folder,
    write_file,
    assemble_text,
    extract_texts,
)
import shutil


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

def test_get_html():
    url = "https://google.com"
    html = get_html(url)
    assert html is not None


def test_setup_folder(tmpdir):
    setup_folder()
    assert os.path.exists('data')


def test_write_file():
    text = "Test content"
    write_file(text)
    file_path = f'data/{hashlib.md5(text.encode()).hexdigest() + ".txt"}'
    assert os.path.exists(file_path)
    shutil.rmtree('data')


def test_assemble_text():
    button = BeautifulSoup(MOCK_HTML, 'html.parser').find('button')
    expected_text = "Button 1\nContent 1Link 1\nlink1\n"
    assert assemble_text(button) == expected_text


def test_extract_texts():
    texts = extract_texts(MOCK_HTML)
    assert texts == [
        "Button 1\nContent 1Link 1\nlink1\n",
        "Button 2\nContent 2Link 2\nlink2\n",
    ]
