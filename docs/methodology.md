# Methodology and scope

## Experimental question and rules

The supplied [call](../protocol/call-for-ai-papers.txt) asks whether AI systems can act as autonomous researchers, authors and reviewers in network and service management. Human Research Directors may select topics and guide prompting; manual editing of the technical content is prohibited. Submissions must disclose models, prompts, frameworks and constraints.

Topics are limited to generative AI/LLMs for NetOps, network/service digital twins, autonomic/cognitive/intent-based management, zero-touch management, and 5G/6G and edge services. The call requests IEEE two-column papers of at most five pages including references and disclosure. These are stated rules, not independently verified properties of every submission.

The 21 submissions retain original form IDs **4–24**. This numbering does not establish that three submissions are missing: the supplied form has 21 data rows.

## Evidence and chronology

| Stage | Evidence and interpretation |
|---|---|
| Call | The supplied version lists submission on 15 August 2026, review notification on 26 August, video submission on 14 September, and the conference on 26–30 October. It retains `[TO-DO]` placeholders. |
| Submission | PDFs and form rows identify titles, submitters, affiliations, topics, declared tools and agreements. Private delivery links, contact fields and administrative timestamps are excluded from the public extract. |
| Review | 21 texts each from ChatGPT, Gemini and Claude, with one supplied common prompt. Exact reviewer checkpoints and runtime settings are not recorded in the review files. |
| Aggregation | The supplied workbook and its source-building logic define equal reviewer weights, selection of 11 and an ascending-ID tie-break. The public reconstruction checks those results. |
| Decision preparation | The supplied notification package contains 11 acceptance and 10 non-acceptance drafts. Its README explicitly says no emails were sent by that workflow. Delivery is not established here. |
| Later video instructions | Notification drafts request 3–4-minute presentations by 28 September 2026, differing from the earlier call deadline. Both documentary stages are retained as such. |
| Presentations | 11 video files match the 11 selected IDs. Their existence does not establish that they were played at the conference. |
| Human discussion | The Spanish document contains panel preparation notes and hypotheses, not a transcript or approved conclusions. |
| Archive preparation | Public arrangement, extraction, indexing and verification: 6 November 2026. No new model reviews were generated. |

Call deadlines, document contents and filesystem modification times are not interchangeable evidence of when an action occurred. Actual submission/review execution dates are not inferred from them.

## Common review rubric

The exact [prompt](../protocol/review-prompt.txt) requests a score and three to four paragraphs for each category, a final score out of 100, and a paragraph about whether the paper belongs among the top 11.

| Category | Maximum |
|---|---:|
| C1 — Technical Correctness, Soundness & Red Flags | 25 |
| C2 — Novelty, Research Value & Core Strengths | 20 |
| C3 — Adherence to Track Rules & Disclosure | 15 |
| C4 — Results, Evaluation, and Honesty on Limitations | 15 |
| C5 — Structure, Clarity, and Formatting | 15 |
| C6 — Discussion Potential for the Panel | 10 |
| **Total** | **100** |

Maxima already encode category weighting. No second weighting or model calibration is applied. Textual recommendations are preserved but do not replace the cohort-wide numerical selection.

## Ranking calculation

```text
review_total[p, r] = C1 + C2 + C3 + C4 + C5 + C6
combined[p] = (ChatGPT[p] + Gemini[p] + Claude[p]) / 3
```

All 63 recorded category sums match their stated final totals. Sort by descending unrounded combined score, breaking ties by ascending paper ID as in the workbook. Select positions 1–11. Category means average the three category scores; reviewer range is the highest minus lowest total. Round only for display.

Selected IDs in rank order: **19, 14, 17, 9, 21, 6, 20, 13, 24, 11, 12**. Paper 12 establishes the 84.00/100 cutoff. Paper 15 is next at 83.333…/100. Archiving applies no new exclusions based on page count, disclosure or reviewer recommendations.

Paper 23's Gemini assignment issue remains in the historical ranking, explicitly flagged. [summary.json](../data/summary.json) separately provides a 20-paper descriptive comparison excluding paper 23 **for every reviewer**. It does not replace the 21-paper ranking.

## Reproducibility limits

The public script reconstructs totals, ranking, selection, indexes and summary statistics from archived reviews and reconciles every relevant cached workbook value. It does not claim to recalculate the workbook in Excel.

The review folders preserve output text, not full requests or conversation histories. Exact model versions, temperature, seeds, browsing settings, tool access, file extraction methods, run dates and prompting history are unavailable. Re-running the common prompt on a current model would be a new experiment.

Generation model names in the form are **self-reported strings**, retained even where unusual or misspelled. They are not reviewer configurations or verified product specifications. Code, datasets, logs and external resources described inside papers are not automatically included. Disclosure statements remain in the PDFs; their claims have not been independently audited.

AI reviews can make factual mistakes or disagree. Preservation does not endorse claims about citations, correctness or human involvement. This collection describes specific outputs and is not a controlled general benchmark of model quality.
