#!/usr/bin/env python3
"""Check coverage, public metadata, relative links and SHA-256 integrity (stdlib only)."""
from __future__ import annotations
import argparse
import csv
import io
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from build_catalog import ROOT, prepare, read_csv, sha

MANIFEST = 'data/manifest-sha256.csv'
IGNORED_DIRS = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', 'dist'}
EMAIL = re.compile(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}')

def public_files():
    paths=[]
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if any(x in IGNORED_DIRS for x in rel.parts) or p.name=='.DS_Store' or p.name.startswith('._'):
            continue
        if p.is_symlink():
            raise ValueError(f'Symlinks are not archival content: {rel}')
        if p.is_file() and str(rel)!=MANIFEST:
            paths.append(p)
    return paths

def slug(text):
    text=re.sub(r'[`*_]','',text.strip()).lower()
    text=re.sub(r'[^\w\- ]','',text,flags=re.UNICODE)
    return text.replace(' ','-')

def validate_structure(files):
    errors=[]
    for p in files:
        rel=p.relative_to(ROOT)
        if p.stat().st_size >= 100*1024*1024:
            errors.append(f'File exceeds ordinary GitHub limit: {rel}')
        if p.name.startswith(('~$','.env')) or p.suffix.lower()=='.eml' or any(x in {'private','author_notifications_CNSM_2026','outputs'} for x in rel.parts) or p.name.startswith('CNSM 2026 - AI Paper Submission'):
            errors.append(f'Private or temporary file in public archive: {rel}')
        if p.suffix in {'.md','.csv','.json','.cff','.txt','.py','.yml'}:
            content=p.read_text(encoding='utf-8')
            if re.search(r'/(?:Users|home)/[^/\s]+/', content):
                errors.append(f'Local absolute user path: {rel}')
            if rel.parts[0] in {'data','docs','zenodo'} and EMAIL.search(content):
                errors.append(f'Contact address in public metadata/documentation: {rel}')
            if re.search(r'https?://[^\s<>"\)]+(?:sharepoint\.com|1drv\.ms|drive\.google\.com)', content, re.I) and rel.parts[0] in {'data','docs','zenodo'}:
                errors.append(f'Private delivery-link pattern in metadata: {rel}')
        if p.suffix=='.md':
            text=re.sub(r'```.*?```','',p.read_text(),flags=re.S)
            for target in re.findall(r'!?\[[^\]\n]+\]\(([^)\n]+)\)',text):
                target=target.strip().strip('<>')
                parsed=urlsplit(target)
                if parsed.scheme or parsed.netloc:
                    continue
                dest=(p.parent/unquote(parsed.path)).resolve() if parsed.path else p
                if not dest.is_relative_to(ROOT):
                    errors.append(f'Link leaves repository: {rel} -> {target}')
                elif dest == ROOT/MANIFEST:
                    pass  # Checked after inventory generation, including on the first build.
                elif not dest.exists():
                    errors.append(f'Broken link: {rel} -> {target}')
                elif parsed.fragment and dest.suffix=='.md':
                    headings={slug(x) for x in re.findall(r'^#{1,6}\s+(.+)$',dest.read_text(),re.M)}
                    if unquote(parsed.fragment) not in headings:
                        errors.append(f'Broken heading anchor: {rel} -> {target}')
    public=read_csv('data/submissions.csv')
    allowed={'paper_id','submitter_names','affiliation','title','title_as_submitted','topic','declared_models','agreements_as_submitted','source_sheet','source_row'}
    if set(public[0]) != allowed:
        errors.append('Public form column whitelist changed')
    metadata=json.loads((ROOT/'zenodo/metadata-draft.json').read_text())
    chairs=read_csv('data/organizers.csv')
    expected=[f"{p['family_names']}, {p['given_names']}" for p in chairs]
    if [p['name'] for p in metadata['creators']]!=expected:
        errors.append('Zenodo creators do not match the four co-chairs')
    participants=read_csv('data/participants.csv')
    if [p['name'] for p in metadata['contributors']]!=[p['name'] for p in participants]:
        errors.append('Zenodo collaborators do not match all 22 participants')
    if any(p['type']!='Researcher' for p in metadata['contributors']):
        errors.append('Unexpected participant role in Zenodo draft')
    if errors:
        raise ValueError('\n'.join(errors))

def manifest_text(files):
    out=io.StringIO(newline='')
    w=csv.DictWriter(out,fieldnames=['path','bytes','sha256'],lineterminator='\n')
    w.writeheader()
    for p in files:
        w.writerow(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
    return out.getvalue()

def validate(write_manifest=False):
    generated,summary=prepare()
    for name,content in generated.items():
        if not (ROOT/name).exists() or (ROOT/name).read_bytes()!=content.encode():
            raise ValueError(f'Stale generated file: {name}. Run scripts/build_catalog.py.')
    files=public_files()
    validate_structure(files)
    expected=manifest_text(files)
    path=ROOT/MANIFEST
    if write_manifest:
        path.write_bytes(expected.encode())
    elif not path.exists() or path.read_bytes()!=expected.encode():
        raise ValueError('Manifest differs from current files. Review changes, then use --write-manifest.')
    print(f'OK: {len(files)} files inventoried; local links, source fidelity, attribution, public-field whitelist and all ranking values checked.')
    return files+[path]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-manifest',action='store_true',help='refresh after reviewed intentional changes')
    args=parser.parse_args()
    try:
        validate(args.write_manifest)
    except (AssertionError,ValueError,KeyError) as e:
        sys.exit(f'Archive validation failed: {e}')

if __name__=='__main__':
    main()
