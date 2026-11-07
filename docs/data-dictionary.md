# Public data dictionary

CSV files use UTF-8, headers, comma separators and standard quoted fields. Some fields contain newlines; use a CSV parser. Numeric values use `.`. Empty issue fields mean no documented flag, not certification of correctness.

## Inputs and provenance

| File | Unit | Fields |
|---|---|---|
| [submissions.csv](../data/submissions.csv) | Submission (21) | `paper_id`; `submitter_names`; `affiliation`; display `title`; verbatim `title_as_submitted`; `topic`; self-reported `declared_models`; verbatim `agreements_as_submitted`; `source_sheet`; Excel `source_row` (header = 1) |
| [participants.csv](../data/participants.csv) | Recorded person (22) | `name`; shared form `affiliation`; semicolon-separated `paper_ids`; `role`; `source` |
| [organizers.csv](../data/organizers.csv) | Co-chair (4) | `name`; `given_names`; `family_names`; `affiliation`; order matches call |
| [paper-inventory.csv](../data/paper-inventory.csv) | PDF (21) | `paper_id`; `page_count`; `text_contains_at_sign` (`true`/`false` from text extraction); `note`. The at-sign indicator is not an exhaustive privacy detector. |
| [provenance.csv](../data/provenance.csv) | Source mapping | `repository_path`; `original_path` relative to source collection; `transformation`; `source_sha256` of original source, which may differ from transformed output |
| [manifest-sha256.csv](../data/manifest-sha256.csv) | Public file | Repository-relative `path`; `bytes`; `sha256`. Excludes itself. |

## Review scores

[review-scores.csv](../data/review-scores.csv): one row per assigned file (63).

| Field | Meaning |
|---|---|
| `paper_id` | Assigned filename ID |
| `reviewer` | `chatgpt`, `gemini`, `claude`; product label, not checkpoint |
| `c1` … `c6` | Category scores; maxima 25, 20, 15, 15, 15, 10 |
| `category_sum` | Sum of category values |
| `reported_final` | Explicit source final score /100 |
| `review_path` | Original text path |
| `assignment_status` | `unverified` for Gemini/paper 23; `not_flagged` otherwise |
| `issue` | `duplicate_of_paper_22_wrong_assignment`, `also_saved_as_paper_23`, or empty |

Original prose and recommendations remain in review files; scores do not endorse those claims.

## Ranking

[ranking.csv](../data/ranking.csv): one row per paper (21), in historical ranking order.

| Field | Meaning |
|---|---|
| `rank` | One-based deterministic position |
| `paper_id`, `title` | Original ID and form-derived display title |
| `combined_score` | Mean of three recorded totals, before display rounding |
| `selection` | `Selected` for ranks 1–11, else `Not selected` |
| `chatgpt_score`, `gemini_score`, `claude_score` | Individual totals |
| `c1_mean` … `c6_mean` | Category averages across reviewers |
| `reviewer_range` | Highest minus lowest reviewer total |
| `score_status` | `contains_unverified_assignment` for paper 23; `as_recorded` otherwise |
| `issue` | Human-readable assignment note or empty |

Paper 23 deliberately retains historical Gemini 99 and mean 66.00, with flags. This is not evidence of three correctly assigned reviews.

## Summary and citation metadata

[summary.json](../data/summary.json) contains counts, selected IDs, cutoff and next score, duplicate paths, and two reviewer analyses: all 21 as recorded, and the same 20 papers excluding paper 23 for every reviewer. Each reports `n`, `mean`, `minimum`, `maximum` and `scores_at_least_95`.

[zenodo/metadata-draft.json](../zenodo/metadata-draft.json) prepares the deposit form: four creators and 22 Researcher contributors. It is not an API payload or an active root `.zenodo.json`. License, publication date, version and DOI remain unset until publication choices are real. See the [guide](publication-guide.es.md).
