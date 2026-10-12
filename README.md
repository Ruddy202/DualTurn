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

The study uses two complementary multiparty datasets. **VoxConverse** provides the main large-scale audio-based evaluation, while **Multi-TPC** adds synchronized multimodal evidence and group-wise robustness analysis.

### VoxConverse

VoxConverse is used for the main audio-based experiments and the detailed analysis of continuous floor-transfer discovery.

The executed protocol uses:

- **177 TRAIN sessions**
- **39 VAL sessions**
- **232 official TEST sessions**

The exact frozen TRAIN and VAL manifests are provided under `configs/voxconverse/`. TEST is taken from the official VoxConverse TEST partition rather than from a separately generated split manifest.

<p align="center">
  <img src="figures/readme/voxconverse_protocol.svg" width="950" alt="VoxConverse evaluation protocol">
</p>

The VoxConverse event construction distinguishes:

- normal floor transfers;
- interruptions;
- backchannels;
- brief interjections; and
- continuations / HOLD events.

The final continuous-discovery reference canonicalizes the TEST set to **6,348 unique SHIFT events**. System 1 produces approximately **80,012 TEST candidates**, covering about **6,092 / 6,348** reference transfers within the strict candidate-ceiling analysis.

#### VoxConverse summary

| Analysis | Primary metric | Result |
|---|---:|---:|
| Task A — supplied-point classification | Macro-F1 | 0.849 |
| Task B — automatic-candidate verification | Event F1 | 0.455 |
| Task C — continuous discovery @ ±0.50 s | Event F1 | 0.552 |
| Task C — continuous discovery @ ±0.70 s | Event F1 | 0.597 |
| Task C — continuous discovery @ ±1.00 s | Event F1 | 0.620 |

At the primary ±0.50 s tolerance, Task C achieves **P = 0.536**, **R = 0.569**, and **F1 = 0.552** with **3,609 TP**, **3,122 FP**, and **2,739 FN**.

The VoxConverse analysis also includes:

- candidate-ceiling analysis;
- silence and speaker-change baselines;
- augmentation comparisons;
- component/verifier analysis;
- event-type diagnostics;
- speaker-count and overlap diagnostics;
- incoming-speaker identification; and
- component-level runtime measurements.

The public VoxConverse release is organized around:

- `voxconverse_main_evaluation.ipynb` — Tasks A/B/C and the main continuous-discovery pipeline;
- `voxconverse_ablation_no_augmentation.ipynb` — no-augmentation condition;
- `voxconverse_ablation_synthetic_only.ipynb` — synthetic-only condition;
- `voxconverse_ablation_waveform_augmentation.ipynb` — timing-preserving waveform augmentation;
- `voxconverse_silence_and_diagnostics.ipynb` — silence baselines and secondary diagnostic analyses.

The notebooks contain code cells only. Task labels in code and retained outputs use historical names: Branch 2 = Task A, Branch 2E = Task B, Branch 1 = Task C, and Branch 3 = the future-activity diagnostic.

The executed VoxConverse pipeline contains bounded contextual/look-ahead evidence in several components. The public notebooks preserve that executed information contract rather than rewriting the historical experiment as strictly past-only. Details are documented in `docs/VOXCONVERSE_PUBLIC_RELEASE_AUDIT.md`.

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

The public Multi-TPC release will contain:

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

`notebooks/voxconverse/` contains the five released VoxConverse notebooks. `notebooks/multitpc/` will be populated after the Multi-TPC release audit.

## Reproducibility and provenance

The public notebooks preserve the experiments that generated the reported results. Sanitization is limited to privacy-sensitive paths, notebook metadata, and removal of Markdown cells, comments, and docstrings; executable code is unchanged apart from the documented path/split-loading cells.

Retained notebook outputs correspond to the original executions. A sanitized notebook is **not** presented as freshly re-executed unless explicitly stated.

See `docs/VOXCONVERSE_REPRODUCIBILITY.md` for VoxConverse setup and `docs/VOXCONVERSE_PUBLIC_RELEASE_AUDIT.md` for provenance and limitations. A corresponding Multi-TPC reproducibility note will accompany the audited Multi-TPC notebook release.

## Data

Dataset audio and annotations are not redistributed in this repository. Users should obtain VoxConverse and Multi-TPC from their respective official sources and configure the dataset and output roots in each notebook's configuration cell (see `docs/VOXCONVERSE_REPRODUCIBILITY.md`).

## Paper results

The repository will retain the executed artifacts used to support the manuscript tables and diagnostic analyses. Numerical values should be traced to the corresponding notebook or frozen result artifact rather than inferred from filenames or development labels.

## Citation

Citation metadata will be added with the final publication record. Until then, please cite the manuscript by title:

> *Leveraging Dual-Process Theory for Multimodal Multiparty Turn-Taking Prediction Using Acoustic and Linguistic Information*

## Release status

Repository assembly is being completed on the `public-release` branch. The VoxConverse notebooks have been added after provenance, privacy, and scientific-consistency review; the Multi-TPC notebooks will follow after their review.
