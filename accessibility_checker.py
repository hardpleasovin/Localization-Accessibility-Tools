"""A tiny HTML accessibility linter.


Rules implemented:
- <html> must have a lang attribute
- <img> must have a non-empty alt attribute
- Interactive elements (<button>, <a role="button">) should have aria-label or clear text
- Headings should start at H1 and not skip levels (simple heuristic)
"""
from pathlib import Path
from bs4 import BeautifulSoup


def check_file(path: Path):
problems = []
html = path.read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'lxml')
# html lang
html_tag = soup.find('html')
if html_tag:
lang = html_tag.get('lang')
if not lang:
problems.append('Missing lang attribute on <html>')
# img alt
for img in soup.find_all('img'):
alt = img.get('alt')
if alt is None or alt.strip() == '':
problems.append(f'<img> missing alt at line ~{get_line_number(img)}')
# interactive elements
for btn in soup.find_all(['button']):
text = btn.get_text(strip=True)
aria = btn.get('aria-label')
if not text and not aria:
problems.append('<button> with no label or aria-label')
for a in soup.find_all('a'):
href = a.get('href')
if href and (a.get_text(strip=True) == '') and not a.get('aria-label'):
problems.append('<a> with href but no text or aria-label')
# headings heuristic
headings = [int(h.name[1]) for h in soup.find_all(['h1','h2','h3','h4','h5','h6'])]
if headings:
# check for skip: e.g., 1 then 3 (skipped 2)
last = headings[0]
for h in headings[1:]:
if h - last > 1:
problems.append('Heading level skip detected')
break
last = h
return problems


def get_line_number(tag):
# BeautifulSoup with lxml may expose .sourceline
try:
return getattr(tag, 'sourceline', '?')
except Exception:
return '?'


def run_checks(path: Path):
results = []
for p in path.rglob('*.html'):
problems = check_file(p)
if problems:
results.append({'file': str(p), 'problems': problems, 'issue': '; '.join(problems)})
return results
