# Known issues and source limitations

## Gemini assignment for paper 23

`reviews/gemini/paper_id_22.txt` and `reviews/gemini/paper_id_23.txt` are byte-identical and discuss paper 22's validator-guided repair study. A distinct Gemini review of paper 23 is absent.

Both files retain their original IDs. [Review scores](../data/review-scores.csv) mark paper 23's Gemini assignment `unverified`; [ranking.csv](../data/ranking.csv) marks its aggregate `contains_unverified_assignment`. Paper 22's duplicate is documented without discarding its relevant review. The 63 files contain **62 distinct byte sequences**.

Paper 23's recorded values are ChatGPT 45, Gemini 99 and Claude 54, yielding 66.00/100. This is a historical workbook value, not a verified three-review score for that paper.

Holding its other two scores fixed, even Gemini 100 gives `(45 + 100 + 54) / 3 = 66.333…`, below the recorded cutoff of 84.00. Correcting only this assignment cannot bring paper 23 into the top 11 under the same rule. Its precise score and rank remain unresolved; no replacement review has been invented.

The supplied notification drafts used an assignment notice for paper 23's Gemini slot. Their delivery is not established. If the correct original review is recovered, preserve provenance, explain the correction and publish a new archive version if the current one has been released.

## Metadata and names

- IDs 4–24 identify 21 form rows. Do not renumber them or infer missing submissions from the first ID.
- Paper 11's form title contains LaTeX-style backslashes. `title_as_submitted` preserves them; display `title` removes only that markup, matching the workbook.
- Some form titles differ from PDF titles, such as “Managements” versus “Management” in paper 18. The form title and original PDF remain unchanged.
- The [participant index](../PARTICIPANTS.md) reflects the submitter field, not every PDF byline. It documents known name differences and unresolved byline roles.
- `declared_models` preserves submitter declarations, typos and unspecified checkpoints without guessing product identities or reviewer settings.
- Source video `paper_id_12.MP4` becomes `paper_id_12.mp4`; bytes are unchanged.

## Documents and execution evidence

- The call retains `[TO-DO]` placeholders and deadlines differing from later notification drafts.
- Papers 5, 7 and 15 have six PDF pages despite the stated five-page limit. The existing ranking is preserved; no new eligibility decision is imposed.
- Submission agreements describe website hosting **for accepted papers**, without a general reuse license for all artifacts. See [RIGHTS.md](../RIGHTS.md).
- Original PDFs can contain contact addresses. Removing contact fields from public tables does not anonymise the PDFs.
- Complete reviewer execution logs, exact reviewer configurations and a panel transcript are absent.
- Panel notes distinguish reported observations and hypotheses from calculations. They are not measured video results or adopted conference conclusions.

Report corrections with the affected ID, path and evidence through [repository issues](https://github.com/NETSERV-UAH/cnsm-2026-cfaip/issues). Do not post private addresses, credentials or original delivery links.
