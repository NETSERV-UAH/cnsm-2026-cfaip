# Recorded results

The [original workbook](CNSM_2026_AI_Paper_Review_Ranking.xlsx) is preserved byte for byte. The public [CSV](../data/ranking.csv) is independently regenerated from the review texts and reconciled against all 21 workbook rows.

Equal reviewer weights; six category maxima 25, 20, 15, 15, 15, 10. Order is descending unrounded mean, then ascending paper ID. The first 11 are selected. See [methodology](../docs/methodology.md).

**Known issue:** the Gemini file assigned to paper 23 is a duplicate of paper 22. The historical ranking is retained; paper 23’s aggregate is not a verified three-review result. [Details and impact](../docs/known-issues.md).

| Rank | Paper | ChatGPT | Gemini | Claude | Mean /100 | Selection |
|---:|---|---:|---:|---:|---:|---|
| 1 | [19 — TwinShield: Static Conditional Admission Assurance for LLM Routing under Imperfect Network Twins](../papers/README.md#paper-19) | 94 | 98 | 99 | 97.00 | Selected |
| 2 | [14 — Rename Before You Reconfigure: Metamorphic Quorums for Selective LLM NetOps](../papers/README.md#paper-14) | 92 | 99 | 97 | 96.00 | Selected |
| 3 | [17 — A Twin Can Be Accurate and Still Wrong: Decision-Conditioned Fidelity for Network Digital Twins](../papers/README.md#paper-17) | 90 | 98 | 99 | 95.67 | Selected |
| 4 | [09 — Verification-Gated Checkpointing for LLM-Based Network Configuration Repair](../papers/README.md#paper-09) | 89 | 99 | 98 | 95.33 | Selected |
| 5 | [21 — When Does LLM Control Pay Off? A Volatility–Cadence Regime Map for Edge Inference Management](../papers/README.md#paper-21) | 88 | 100 | 97 | 95.00 | Selected |
| 6 | [06 — The Null Operator: A Do-Nothing Baseline for Zero-Touch Management](../papers/README.md#paper-06) | 84 | 99 | 94 | 92.33 | Selected |
| 7 | [20 — Server-to-Edge Ranking Transfer for Telecom LLMs](../papers/README.md#paper-20) | 86 | 99 | 91 | 92.00 | Selected |
| 8 | [13 — Bober-Clos: Copy the Canals, Not the Congestion? A Beaver-Inspired Fronthaul Fabric Under Stress](../papers/README.md#paper-13) | 84 | 100 | 89 | 91.00 | Selected |
| 9 | [24 — IRIS: Intent-Driven Closed-Loop QoE Management of Volumetric XR Streaming at the Private-5G Edge](../papers/README.md#paper-24) | 78 | 99 | 95 | 90.67 | Selected |
| 10 | [11 — Beyond What-If: A Survey and Research Agenda for Out-of-the-Box Uses of Network Digital Twins](../papers/README.md#paper-11) | 83 | 96 | 90 | 89.67 | Selected |
| 11 | [12 — An LLM Agent for Root-Cause Diagnosis of Network Failures from System and Network Logs](../papers/README.md#paper-12) | 63 | 98 | 91 | 84.00 | Selected |
| 12 | [15 — How Stale Is Too Stale? Residual-Calibrated Service Re-Placement for Edge Services Under Control-Loop Lag](../papers/README.md#paper-15) | 65 | 93 | 92 | 83.33 | Not selected |
| 13 | [07 — Confidence-Aware Network Digital Twins for Safe Autoscaling of 5G Core Services](../papers/README.md#paper-07) | 72 | 93 | 80 | 81.67 | Not selected |
| 14 | [10 — SPEAR-5G: A Stackelberg Game-Theoretic Framework for Attack-Resilient Deployment of Non-Public 5G Networks](../papers/README.md#paper-10) | 58 | 91 | 82 | 77.00 | Not selected |
| 15 | [04 — Do Network Elements Have a Grammatical Fingerprint? A Pre-Registered Test on Cellular Telemetry](../papers/README.md#paper-04) | 72 | 72 | 84 | 76.00 | Not selected |
| 16 | [22 — Validator-Guided Repair on a Shared Initial LLM Candidate: A Preregistered Paired Evaluation for Network Configuration Safety](../papers/README.md#paper-22) | 61 | 99 | 60 | 73.33 | Not selected |
| 17 | [18 — Synthetic Multi-Layer Operational Data for Internet Infrastructure Managements: Needs, Methods and Limitations](../papers/README.md#paper-18) | 58 | 80 | 74 | 70.67 | Not selected |
| 18 | [23 — Neuro-Symbolic Orchestration for Safe Autonomous NetOps Using LLMs and Fuzzy Control](../papers/README.md#paper-23) | 45 | 99* | 54 | 66.00* | Not selected |
| 19 | [05 — Beyond Zero-Touch: Grand Challenges for Network and Service Management in the Next Decade](../papers/README.md#paper-05) | 45 | 73 | 52 | 56.67 | Not selected |
| 20 | [16 — EvoTwin: Agentic Discovery of Sovereign Neuro-Symbolic Digital Twins for Resilient and Sustainable NetOps](../papers/README.md#paper-16) | 46 | 60 | 50 | 52.00 | Not selected |
| 21 | [08 — Adaptive Memory Retention in Diffusion–MARL with Validation for Long-Horizon Decision Making](../papers/README.md#paper-08) | 34 | 60 | 50 | 48.00 | Not selected |

*Unverified Gemini assignment. Cutoff: 84.00/100 (paper 12). First not selected: 83.33/100 (paper 15).

Reproduce and validate with `python3 scripts/build_catalog.py --check`. This reconstructs aggregation, not the original model runs.

