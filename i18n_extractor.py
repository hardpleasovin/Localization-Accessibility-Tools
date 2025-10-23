"""Very small i18n extractor for demo purposes.


- Finds text nodes in HTML and extracts short strings.
- Finds lines in .txt files separated by newlines.


This is intentionally minimal — real projects should use tools
that parse templates for variable markers, skip code, etc.
"""
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Tuple
import polib


def extract_from_html_file(path: Path) -> List[Tuple[str, str]]:
entries = []
html = path.read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'lxml')
# Extract text from common visible tags
for tag in soup.find_all(['p', 'span', 'h1', 'h2', 'h3', 'a', 'button', 'label']):
text = tag.get_text(strip=True)
if text and len(text) > 1 and len(text) < 200:
entries.append((str(path), text))
return entries


def extract_from_txt_file(path: Path) -> List[Tuple[str, str]]:
entries = []
for line in path.read_text(encoding='utf-8').splitlines():
line = line.strip()
if line:
entries.append((str(path), line))
return entries


def extract_from_path(path: Path):
all_entries = []
for p in path.rglob('*'):
if p.suffix.lower() in ['.html', '.htm']:
all_entries.extend(extract_from_html_file(p))
elif p.suffix.lower() in ['.txt']:
all_entries.extend(extract_from_txt_file(p))
# dedupe by message
seen = set()
unique = []
for src, msg in all_entries:
if msg not in seen:
seen.add(msg)
unique.append((src, msg))
return unique


def write_pot(entries, out_path: Path):
pot = polib.POFile()
pot.metadata = {
'Project-Id-Version': 'localization-accessibility-tools 0.1',
'Report-Msgid-Bugs-To': '',
'POT-Creation-Date': '',
'PO-Revision-Date': '',
'Last-Translator': '',
'Language': '',
}
for src, msg in entries:
entry = polib.POEntry(msgid=msg, msgstr='')
entry.comment = f'Source: {src}'
pot.append(entry)
out_path.parent.mkdir(parents=True, exist_ok=True)
pot.save(str(out_path))
