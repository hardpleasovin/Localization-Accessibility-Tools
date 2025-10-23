# Localization & Accessibility Tools

A compact toolkit for open-source maintainers to:
- Extract strings for translation from simple source formats.
- Produce `.pot` skeleton files for translators.
- Run a lightweight HTML accessibility scan to catch basic issues early in CI.
This project is intentionally small and dependency-light so it can be included in CI pipelines or run locally.
## Quickstart
1. Install dependencies (Python 3.9+):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Run the CLI help:
python -m locaccess.cli --help
Example: extract strings and check sample HTML
python -m locaccess.cli extract sample --out translations/messages.pot
python -m locaccess.cli check sample
What it does
extract: walks a directory, finds .html and .txt (or simple templated .tpl) files and extracts translatable strings into a .pot file.
check: scans HTML files and reports missing alt attributes for <img>, missing lang on <html>, skipped headings order, and missing aria-* on interactive elements.
Contribution & Sponsorship
If you like this starter and want ongoing improvements (more extractors, support for React/Vue, integration with translation platforms, or more accessibility rules), consider sponsoring via GitHub Sponsors.
