#!/usr/bin/env python3
"""Rebuild public tables and indexes from the archived evidence. Python 3.10+, stdlib only."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import re
import statistics
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
MODELS = ('chatgpt', 'gemini', 'claude')
LABELS = ('ChatGPT', 'Gemini', 'Claude')
MAXIMA = (25, 20, 15, 15, 15, 10)
IDS = set(range(4, 25))

def read_csv(name):
    with (ROOT / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def csv_text(rows):
    out = io.StringIO(newline='')
    w = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    return out.getvalue()

def md(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def cached_sheets(path):
    """Read existing XLSX cell caches without changing or recalculating the source."""
    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    rid = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
    result = {}
    with ZipFile(path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels = {r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        book = ET.fromstring(z.read('xl/workbook.xml'))
        for sheet in book.find('s:sheets', ns):
            target = rels[sheet.attrib[rid]]
            target = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            cells = {}
            for cell in ET.fromstring(z.read(target)).findall('.//s:sheetData/s:row/s:c', ns):
                value = cell.find('s:v', ns)
                kind = cell.get('t')
                if kind == 'inlineStr':
                    cells[cell.get('r')] = ''.join(cell.find('s:is', ns).itertext())
                elif value is not None and value.text is not None:
                    text = value.text
                    cells[cell.get('r')] = strings[int(text)] if kind == 's' else (text if kind in ('str','e') else float(text))
            result[sheet.get('name')] = cells
    return result

def prepare():
    submissions = read_csv('data/submissions.csv')
    assert len(submissions) == 21 and {int(p['paper_id']) for p in submissions} == IDS
    by_id = {int(p['paper_id']):p for p in submissions}
    participants = read_csv('data/participants.csv')
    assert len(participants) == 22 and len({p['name'] for p in participants}) == 22
    assert {int(i) for p in participants for i in p['paper_ids'].split(';')} == IDS
    for p in participants:
        for i in p['paper_ids'].split(';'):
            assert p['name'] in by_id[int(i)]['submitter_names'], (p['name'], i)
    scores, indexed = [], {}
    duplicate_groups = {}
    for model in MODELS:
        files = list((ROOT / 'reviews' / model).glob('*.txt'))
        assert {int(p.stem.split('_')[-1]) for p in files} == IDS and len(files) == 21
        for pid in sorted(IDS):
            source = f'reviews/{model}/paper_id_{pid}.txt'
            text = (ROOT / source).read_text().replace('**','').replace('__','')
            matches = re.findall(r'(?i)\bscore\s*:\s*(\d+(?:\.\d+)?)\s*/\s*(\d+)', text)
            categories = [(float(v), int(m)) for v,m in matches if int(m) != 100]
            final = [float(v) for v,m in matches if int(m) == 100]
            assert tuple(m for v,m in categories) == MAXIMA, source
            assert len(final) == 1 and all(0 <= v <= m for v,m in categories), source
            assert sum(v for v,m in categories) == final[0], source
            issue = 'duplicate_of_paper_22_wrong_assignment' if (model,pid)==('gemini',23) else ('also_saved_as_paper_23' if (model,pid)==('gemini',22) else '')
            row = dict(paper_id=pid, reviewer=model, **{f'c{i+1}':v for i,(v,m) in enumerate(categories)},
                category_sum=sum(v for v,m in categories), reported_final=final[0], review_path=source,
                assignment_status='unverified' if (model,pid)==('gemini',23) else 'not_flagged', issue=issue)
            scores.append(row)
            indexed[pid,model] = row
            duplicate_groups.setdefault(sha(ROOT / source), []).append(source)
    duplicates = [sorted(v) for v in duplicate_groups.values() if len(v)>1]
    assert duplicates == [['reviews/gemini/paper_id_22.txt','reviews/gemini/paper_id_23.txt']], duplicates
    ranking = []
    ordered = sorted(IDS, key=lambda pid:(-sum(indexed[pid,m]['reported_final'] for m in MODELS),pid))
    for rank,pid in enumerate(ordered,1):
        totals = [indexed[pid,m]['reported_final'] for m in MODELS]
        ranking.append(dict(rank=rank,paper_id=pid,title=by_id[pid]['title'],combined_score=sum(totals)/3,
            selection='Selected' if rank<=11 else 'Not selected',
            **{f'{m}_score':indexed[pid,m]['reported_final'] for m in MODELS},
            **{f'c{i+1}_mean':sum(indexed[pid,m][f'c{i+1}'] for m in MODELS)/3 for i in range(6)},
            reviewer_range=max(totals)-min(totals),
            score_status='contains_unverified_assignment' if pid==23 else 'as_recorded',
            issue='Gemini review also saved as paper 23' if pid==22 else ('Gemini review duplicates paper 22 and describes that paper' if pid==23 else '')))

    # Independently reconcile every score, category, rank and selection to the supplied workbook.
    wb = cached_sheets(ROOT / 'results/CNSM_2026_AI_Paper_Review_Ranking.xlsx')
    for label,model in zip(LABELS,MODELS):
        cells = wb[label]
        for n in range(8,29):
            pid = int(cells[f'A{n}'])
            s = indexed[pid,model]
            assert cells[f'B{n}'] == by_id[pid]['title']
            for i,col in enumerate('CDEFGH',1):
                assert cells[f'{col}{n}'] == s[f'c{i}'], (model,pid,col)
            assert cells[f'I{n}'] == cells[f'J{n}'] == s['reported_final']
            assert cells[f'K{n}'] == 0
    cells = wb['Combined ranking']
    assert cells['D5'] == 11 and cells['G5'] == 84 and cells['J5'] == 11
    for n,row in enumerate(ranking,8):
        expected = [row['rank'],row['paper_id'],row['title'],row['combined_score'],row['selection'],
                    *[row[f'{m}_score'] for m in MODELS], *[row[f'c{i}_mean'] for i in range(1,7)], row['reviewer_range']]
        for col,value in zip('ABCDEFGHIJKLMNO',expected):
            actual = cells[f'{col}{n}']
            assert math.isclose(actual,value,abs_tol=1e-9) if isinstance(value,(int,float)) else actual==value, (n,col,actual,value)
    selected = {r['paper_id'] for r in ranking if r['selection']=='Selected'}
    videos = list((ROOT/'videos').glob('*.mp4'))
    assert len(videos) == 11 and {int(p.stem.split('_')[-1]) for p in videos} == selected
    assert len(list((ROOT/'papers').glob('*.pdf'))) == 21
    assert {int(p.stem.split('_')[-1]) for p in (ROOT/'papers').glob('*.pdf')} == IDS
    # Verify preservation of every imported original.
    for item in read_csv('data/provenance.csv'):
        if item['transformation']=='byte-identical copy':
            assert sha(ROOT/item['repository_path']) == item['source_sha256'], item['repository_path']

    summary = dict(submissions=21,participants=22,review_files=63,distinct_review_files=62,selected_papers=11,
        videos=11,selected_ids_in_rank_order=[r['paper_id'] for r in ranking[:11]],selection_cutoff=84,
        first_not_selected_score=ranking[11]['combined_score'],duplicates=duplicates,reviewer_statistics={})
    for label,pids in [('all_21_as_recorded',sorted(IDS)),('20_excluding_paper_23_for_every_reviewer',sorted(IDS-{23}))]:
        summary['reviewer_statistics'][label] = {}
        for model in MODELS:
            vals = [indexed[pid,model]['reported_final'] for pid in pids]
            summary['reviewer_statistics'][label][model] = dict(n=len(vals),mean=statistics.mean(vals),minimum=min(vals),maximum=max(vals),scores_at_least_95=sum(v>=95 for v in vals))

    generated = {'data/review-scores.csv':csv_text(scores),'data/ranking.csv':csv_text(ranking),'data/summary.json':json.dumps(summary,ensure_ascii=False,indent=2)+'\n'}
    ranks = {r['paper_id']:r for r in ranking}
    catalog = ['# Paper catalogue\n', 'All 21 submissions are preserved, including those not selected. IDs are the original form IDs (4–24). Names identify human submitters / Research Directors, not assertions of human authorship of the AI-generated text.\n',
        'Scores and decisions reproduce the supplied ranking. **Paper 23 has an unverified Gemini assignment**; see [known issues](../docs/known-issues.md). Model names below are self-reported submission metadata.\n',
        '| ID | Title | Submitters | Decision | Mean /100 |', '|---|---|---|---|---:|']
    for pid,p in by_id.items():
        r=ranks[pid]
        catalog.append(f"| [Paper {pid:02d}](#paper-{pid:02d}) | {md(p['title'])} | {md(p['submitter_names'])} | {r['selection']} | {r['combined_score']:.2f}{'*' if pid==23 else ''} |")
    catalog += ['\n*Paper 23: recorded aggregate, not a verified three-paper-specific-review score.\n']
    for pid,p in by_id.items():
        r=ranks[pid]
        review_links=' · '.join(f'[{label}](../reviews/{m}/paper_id_{pid}.txt)' for label,m in zip(LABELS,MODELS))
        video=f' · [Video](../videos/paper_id_{pid}.mp4)' if pid in selected else ''
        catalog += [f'## Paper {pid:02d}\n',f"**{md(p['title'])}**\n",f"Research Directors / submitters: {md(p['submitter_names'])}.\n",f"Affiliation as submitted: {md(p['affiliation'])}.\n",f"Topic: {md(p['topic'])}.\n",f"Declared generation tools: {md(p['declared_models'])}\n",f"[Original PDF](paper_id_{pid}.pdf) · Reviews: {review_links}{video}\n",f"Recorded rank: {r['rank']}/21; mean: {r['combined_score']:.2f}/100; {r['selection']}."+(' Gemini assignment is unverified.' if pid==23 else '')+'\n']
    generated['papers/README.md']='\n'.join(catalog)+'\n'

    credits=['# Participants and acknowledgements\n','Thank you to every person who submitted work to the CNSM 2026 **The Agentic AI Researcher** experiment. The contributions of selected and non-selected submissions are equally part of this archive.\n',
        'The table lists **22 distinct people across 21 submissions**, alphabetically by the recorded full name. It is derived from the submission form, including every person explicitly named in a joint submission. Repeated submitters are listed once. Spellings are preserved; no ORCID identifiers have been inferred.\n',
        '| Participant | Affiliation / organisation as submitted | Paper IDs |','|---|---|---|']
    for p in participants:
        links=', '.join(f'[{int(i):02d}](papers/README.md#paper-{int(i):02d})' for i in p['paper_ids'].split(';'))
        credits.append(f"| {md(p['name'])} | {md(p['affiliation'])} | {links} |")
    credits += ['\nJoint-submission affiliations are reproduced as a shared field; they are not individual affiliation assignments. The form spells the paper 11 submitter “Suthar Jainish Chandraprakash”; the PDF uses “Jainish Suthar”. We retain the form spelling for this index.\n',
        '## Special Track Co-Chairs and archive creators\n','The archive citation lists the four co-chairs, in the order of the supplied call. The 22 submitters are identified as collaborators in the prepared Zenodo metadata. This credits their participation and does not make them responsible for other submissions or AI review statements.\n']
    for p in read_csv('data/organizers.csv'):
        credits.append(f"- **{p['name']}** — {p['affiliation']}")
    credits += ['\n## Names recorded within the papers\n','The original PDFs retain their own bylines and acknowledgements. These differ from the form’s submitter field. For example, Alberto Leon-Garcia appears alongside David Luo in papers 20 and 21; Benjamin Grando Moreira is named as academic advisor in paper 12. The paper 17 byline also contains “Vilena Vasquez” and “Juno Patinhas”, whose roles are not resolved by the submission form. They are preserved in the PDF and not silently classified as human submitters.\n',
        'The participant table is a complete index of the supplied submitter field, not a replacement for PDF bylines or a verified list of every human contributor. For name, role, or affiliation corrections, use a [repository issue](https://github.com/NETSERV-UAH/cnsm-2026-cfaip/issues). Do not post private contact details.\n',
        '## Credit and citation\n','See [CITATION.cff](CITATION.cff) for the archive citation and [Zenodo metadata](zenodo/metadata-draft.json) for the separate creator/contributor roles. Zenodo contributors appear in the record but not in the generated bibliographic citation. A dataset DOI identifies this collection; it does not create a separate proceedings DOI for each paper.\n']
    generated['PARTICIPANTS.md']='\n'.join(credits)+'\n'
    results=['# Recorded results\n','The [original workbook](CNSM_2026_AI_Paper_Review_Ranking.xlsx) is preserved byte for byte. The public [CSV](../data/ranking.csv) is independently regenerated from the review texts and reconciled against all 21 workbook rows.\n',
        'Equal reviewer weights; six category maxima 25, 20, 15, 15, 15, 10. Order is descending unrounded mean, then ascending paper ID. The first 11 are selected. See [methodology](../docs/methodology.md).\n',
        '**Known issue:** the Gemini file assigned to paper 23 is a duplicate of paper 22. The historical ranking is retained; paper 23’s aggregate is not a verified three-review result. [Details and impact](../docs/known-issues.md).\n',
        '| Rank | Paper | ChatGPT | Gemini | Claude | Mean /100 | Selection |','|---:|---|---:|---:|---:|---:|---|']
    for r in ranking:
        pid=r['paper_id']
        results.append(f"| {r['rank']} | [{pid:02d} — {md(r['title'])}](../papers/README.md#paper-{pid:02d}) | {r['chatgpt_score']:g} | {r['gemini_score']:g}{'*' if pid==23 else ''} | {r['claude_score']:g} | {r['combined_score']:.2f}{'*' if pid==23 else ''} | {r['selection']} |")
    results += ['\n*Unverified Gemini assignment. Cutoff: 84.00/100 (paper 12). First not selected: 83.33/100 (paper 15).\n','Reproduce and validate with `python3 scripts/build_catalog.py --check`. This reconstructs aggregation, not the original model runs.\n']
    generated['results/README.md']='\n'.join(results)+'\n'
    video_index=['# AI-generated presentations\n','These 11 supplied MP4 files correspond exactly to the 11 selected papers. Files are unchanged; the source extension `paper_id_12.MP4` was normalised to lowercase. Presence here records receipt of a file, not verification of which tool produced it or whether it was played at the conference.\n',
        '| Paper | Title | Size (MiB) | Video |','|---|---|---:|---|']
    for r in ranking[:11]:
        pid=r['paper_id'];size=(ROOT/f'videos/paper_id_{pid}.mp4').stat().st_size/(1024**2)
        video_index.append(f"| [{pid:02d}](../papers/README.md#paper-{pid:02d}) | {md(r['title'])} | {size:.2f} | [MP4](paper_id_{pid}.mp4) |")
    video_index += ['\nAll videos are ordinary Git files, with no Git LFS pointer dependency. Download an individual MP4 if GitHub cannot preview it. [Publication instructions](../docs/publication-guide.es.md) explain size limits and Zenodo preservation.\n']
    generated['videos/README.md']='\n'.join(video_index)+'\n'
    return generated,summary

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='validate without writing; fail if generated files differ')
    args=parser.parse_args()
    generated,summary=prepare()
    mismatches=[]
    for name,text in generated.items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_bytes()!=text.encode():mismatches.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(text.encode())
    if mismatches:
        sys.exit('Generated files need rebuilding: '+', '.join(mismatches))
    print(f"OK: {summary['submissions']} papers; {summary['participants']} participants; 63 review files; 11 videos; workbook reconciled; known duplicate preserved.")

if __name__=='__main__':
    main()
