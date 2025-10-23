"""Simple CLI for the Localization & Accessibility Tools"""
import sys
import pathlib
import click
from . import i18n_extractor, accessibility_checker


@click.group()
def main():
"""locaccess CLI"""
pass


@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--out', '-o', default='messages.pot', help='Output .pot file')
def extract(path, out):
"""Extract translatable strings from files in PATH and write a POT file to OUT."""
path = pathlib.Path(path)
pot_path = pathlib.Path(out)
entries = i18n_extractor.extract_from_path(path)
i18n_extractor.write_pot(entries, pot_path)
click.echo(f'Wrote {len(entries)} entries to {pot_path}')


@main.command()
@click.argument('path', type=click.Path(exists=True))
def check(path):
"""Run accessibility checks on HTML files inside PATH."""
path = pathlib.Path(path)
report = accessibility_checker.run_checks(path)
for item in report:
click.echo(f"{item['file']}: {item['issue']}")
click.echo(f"Found {sum(len(r['problems']) for r in report)} problems in {len(report)} files")


if __name__ == '__main__':
main()
