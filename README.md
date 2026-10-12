# DualTurn

Research code and reproducibility artifacts for:

**Leveraging Dual-Process Theory for Multimodal Multiparty Turn-Taking Prediction Using Acoustic and Linguistic Information**

This repository accompanies work on continuous multiparty turn-taking using a dual-process-inspired computational architecture. A fast candidate-discovery stage proposes plausible transition opportunities, and a selective verification stage evaluates those candidates using complementary contextual evidence.

<p align="center">
  <img src="figures/readme/dualturn_overview.svg" width="950" alt="DualTurn discovery and verification architecture">
</p>

## Evaluation tasks

The repository separates three evaluation settings:

- **Task A — supplied-point classification:** a decision time is provided and the system predicts SHIFT or HOLD.
- **Task B — automatic-candidate verification:** automatically proposed candidate points are classified as genuine or non-genuine floor transfers.
- **Task C — continuous discovery:** the system discovers, verifies, and localizes floor-transfer events on the continuous interaction timeline.

Task C uses one-to-one temporal event matching, with **±0.50 s** as the primary tolerance and **±0.70 s / ±1.00 s** as sensitivity analyses.

<p align="center">
  <img src="figures/readme/tasks_abc.svg" width="950" alt="Task A, Task B and Task C evaluation settings">
</p>

## Datasets

### VoxConverse

VoxConverse is used for the main audio-based experiments. The repository preserves the exact frozen development split used by the executed experiments:

- TRAIN: 177 sessions
- VAL: 39 sessions
- TEST: official VoxConverse TEST partition

The TRAIN and VAL session manifests are provided under `configs/voxconverse/`.

The final continuous-discovery evaluation canonicalizes the TEST reference to **6,348 unique SHIFT events** and evaluates predictions with one-to-one temporal matching.

### Multi-TPC

Multi-TPC complements VoxConverse with synchronized multimodal interaction from **seven triadic conversational groups**. The local audited release used in the experiments contains **23 complete sessions**.

The Multi-TPC analysis is intentionally separated into three protocols:

1. **Original group-disjoint held-out evaluation** — five groups for training, one for validation, and one pre-reserved group for final evaluation.
2. **Post-hoc seven-group nested evaluation** — each group serves once as the outer held-out group, with model/configuration selection restricted to the remaining groups.
3. **Fixed-configuration ablation analysis** — evaluates stage and modality contributions under a common configuration.

<p align="center">
  <img src="figures/readme/multitpc_protocol.svg" width="950" alt="Multi-TPC evaluation protocol">
</p>

Multi-TPC uses native participant-state annotations to derive two principal floor-transfer types:

- **NTT — normal turn transfer:** the outgoing speaker releases the floor and another participant subsequently takes it.
- **ITT — interruption turn transfer:** the incoming participant begins before the incumbent releases the floor and sustains the new primary turn.

As in VoxConverse, continuous discovery is evaluated at **±0.50 s**, with **±0.70 s** and **±1.00 s** sensitivity tolerances.

#### Multi-TPC summary

| Analysis | Task A | Task B | Task C F1 @ ±0.50 s | Task C F1 @ ±1.00 s |
|---|---:|---:|---:|---:|
| Original group-disjoint held-out | 0.500 | 0.563 | 0.260 | 0.445 |
| Post-hoc seven-group nested | 0.572 ± 0.045 | 0.607 ± 0.021 | 0.343 ± 0.040 | 0.504 ± 0.050 |

The seven-group analysis is **robustness evidence rather than a second untouched confirmatory test set**. Method ordering varies across groups, and no paired method comparison in that analysis survives Holm correction.

The fixed-configuration ablations provide complementary evidence about stage and modality contributions. Individual modality effects are treated as descriptive because their magnitude varies across groups and no ablation comparison survives Holm correction.

The public Multi-TPC release will contain three notebooks:

- `multitpc_heldout_evaluation.ipynb` — original group-disjoint held-out evaluation;
- `multitpc_seven_group_evaluation.ipynb` — post-hoc seven-group nested analysis;
- `multitpc_ablation.ipynb` — fixed-configuration stage/modality ablations.

## Repository layout

```text
DualTurn/
├── README.md
├── configs/
│   └── voxconverse/
│       ├── train_sessions.json
│       └── val_sessions.json
├── notebooks/
│   ├── voxconverse/
│   └── multitpc/
├── results/
├── figures/
│   └── readme/
└── docs/
```

The notebook directories are populated with sanitized copies of the executed research notebooks after release auditing.

## Reproducibility and provenance

The public notebooks are intended to preserve the experiments that generated the reported results. Sanitization is limited to privacy-sensitive paths, notebook metadata, development-only commentary, and public-facing naming where this does not alter computation.

Retained notebook outputs correspond to the original executions. A sanitized notebook is **not** presented as freshly re-executed unless explicitly stated.

The current VoxConverse implementation uses candidate-centred and bounded contextual evidence in several components. The repository therefore documents the executed information contract directly rather than retroactively rewriting the implementation as strictly past-only.

See `docs/VOXCONVERSE_REPRODUCIBILITY.md` for VoxConverse-specific provenance and limitations. A corresponding Multi-TPC reproducibility note will accompany the audited Multi-TPC notebook release.

## Data

Dataset audio and annotations are not redistributed in this repository. Users should obtain VoxConverse and Multi-TPC from their respective official sources and arrange them according to the paths documented with each notebook.

## Paper results

The repository will retain the exact executed artifacts used to support the manuscript tables and diagnostic analyses. Numerical values should be traced to the corresponding notebook or frozen result artifact rather than inferred from filenames or development labels.

## Citation

Citation metadata will be added with the final publication record. Until then, please cite the manuscript by title:

> *Leveraging Dual-Process Theory for Multimodal Multiparty Turn-Taking Prediction Using Acoustic and Linguistic Information*

## Release status

Repository assembly is currently being completed on the `public-release` branch. Experimental notebooks are added only after provenance, privacy, and scientific-consistency review.
