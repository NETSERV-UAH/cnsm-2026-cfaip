# Provenance and transformations

Prepared from the organiser's supplied local collection on **2026-11-06**. Existing evidence is arranged with public metadata and navigation; no papers or reviews were regenerated.

| Source | Public location | Treatment |
|---|---|---|
| `CfAIP_v2p.txt` | `protocol/call-for-ai-papers.txt` | Exact bytes, descriptive filename |
| `prompt.txt` | `protocol/review-prompt.txt` | Exact bytes, descriptive filename |
| `papers/` | `papers/` | All 21 PDFs, exact bytes and IDs |
| `chatgpt_results/`, `gemini_results/`, `claude_results/` | `reviews/chatgpt/`, `reviews/gemini/`, `reviews/claude/` | All 63 originals, including duplicate |
| Final workbook in `outputs/01a09bba/` | `results/` | Exact bytes, including formulas, caches and issue flags |
| `videos/` | `videos/` | All 11 originals; paper 12 extension normalised to lowercase |
| Submission form workbook | `data/submissions.csv`, `data/participants.csv` | Public-field extract; original workbook excluded |
| Spanish panel notes | `discussion/panel-reflections.es.md` | Archive context added; local links replaced; source link label adapted |
| Notification drafts | [Decision context](decisions.md) | Process summarised; private drafts excluded |
| Historical build scripts and temporary outputs | [Public reconstruction script](../scripts/build_catalog.py) | Aggregation reimplemented without private-form dependency or machine-specific paths |

**98 imported files are byte-identical:** 21 papers, 63 reviews, 11 videos, two protocol texts and one workbook. [provenance.csv](../data/provenance.csv) records source mappings and hashes, including transformed form/notes sources. Original source hashes identify versions without publishing the private workbook.

## Public form extraction

An explicit whitelist selects fields from the 14-column original:

| Original column | Public treatment |
|---|---|
| A — ID | `paper_id` |
| B, C — Start/completion times | Excluded |
| D, E — Form-account email/name | Excluded |
| F — Last modification time | Excluded |
| G — Submitter Name (Research Director) | `submitter_names`, surrounding whitespace trimmed |
| H — Contact Email Address | Excluded |
| I — Affiliation / Organization | `affiliation`, surrounding whitespace trimmed |
| J — Paper Title | Verbatim `title_as_submitted`; display `title` strips backslashes and surrounding whitespace |
| K — Topic | `topic` |
| L — Primary models/frameworks | `declared_models`, surrounding whitespace trimmed; embedded newlines retained |
| M — Link to submitted PDF | Excluded; public links target archived PDFs |
| N — Mandatory Agreements | `agreements_as_submitted`, verbatim and in original order |

`source_sheet` and `source_row` identify the original row. All 21 rows record the four agreements. These are declarations, not independent verification of compliance or a broader licensing grant.

The custodian can compare the extract to the original using these row and column mappings. Public readers can reconstruct rankings and indexes without the private workbook. The initial extraction itself requires that private source and is not claimed to be independently reproducible from public files alone.

## Participant extraction

Paper 8 explicitly lists three people; paper 24 lists two. Both are split into individual rows. Rob White (13, 14) and David Luo (20, 21) each appear once with both IDs. Other full names are not split on whitespace. This yields 22 distinct recorded people.

Joint affiliations remain the shared form string; no person-specific assignment is inferred. The list is sorted by full recorded name, not acceptance, rank or seniority. [organizers.csv](../data/organizers.csv) preserves co-chair names, affiliations and order from the call.

## Integrity and maintenance

[manifest-sha256.csv](../data/manifest-sha256.csv) inventories public files by path, byte size and SHA-256, excluding itself, `.git/`, caches and ignored local build outputs. It covers documentation and scripts as well as research artifacts.

After an intentional correction, rebuild derived files, refresh the manifest and record the reason in [CHANGELOG.md](../CHANGELOG.md). Do not replace released originals silently. Integrity checks do not establish scientific correctness or consent.
