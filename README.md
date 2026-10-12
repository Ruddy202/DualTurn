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

The final continuous-discovery reference canonicalizes the TEST set to **6,348 unique SHIFT events**. System 1 produces **80,012 TEST candidates**, which cover **6,092 / 6,348** reference transfers (0.960) at ±0.50 s.

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

The executed VoxConverse pipeline contains bounded contextual/look-ahead evidence in several components. The public notebooks preserve that executed information contract rather than rewriting the historical experiment as strictly past-only. The affected components are the candidate-centred WavLM windows, right-side ASR context used by the Qwen-derived scores, some post-candidate System-2 features, symmetric neighbouring-candidate context in the temporal verifier, and post-candidate evidence in the RR-FAP diagnostics. No TEST ground-truth labels enter the TEST feature or prediction path.

### Multi-TPC

Multi-TPC complements VoxConverse with synchronized multimodal interaction from **seven triadic conversational groups**. The local audited release used in the experiments contains **23 complete sessions**.

The Multi-TPC analysis is intentionally separated into three protocols:

1. **Original group-disjoint held-out evaluation** — five groups for training, one for validation, and one pre-reserved group for final evaluation.
2. **Post-hoc seven-group nested evaluation** — each group serves once as the outer held-out group, with model/configuration selection restricted to the remaining groups.
3. **Fixed-configuration ablation analysis** — evaluates stage and modality contributions under a common configuration.

The seven-group and ablation analyses evaluate a revised version of the proposed system, developed after the original held-out evaluation. The two summary rows below therefore come from different system versions and are not repeated measurements of one frozen model.

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

The public Multi-TPC release contains:

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
├── third_party/
│   └── muvap/
├── figures/
│   └── readme/
└── docs/
    ├── VOXCONVERSE_REPRODUCIBILITY.md
    └── MULTITPC_REPRODUCIBILITY.md
```

`notebooks/voxconverse/` contains the five released VoxConverse notebooks and `notebooks/multitpc/` the three Multi-TPC notebooks. `third_party/muvap/` vendors the exact MuVAP source (MIT licence) used by the Multi-TPC comparators.

## Requirements

The VoxConverse experiments were run with Python 3.11 and PyTorch 2.7 (CUDA 11.8) on a single 12 GB NVIDIA GPU. The main dependencies are:

- `numpy`, `pandas`, `scipy`, `scikit-learn`, `lightgbm`, `matplotlib`, `seaborn`;
- `torch`, `torchaudio`, `soundfile`;
- `transformers`, `peft`, `datasets` (WavLM, Qwen3 LoRA);
- `faster-whisper` (ASR), `pyannote.audio` (diarization), `speechbrain` (ECAPA-TDNN).

Gated Hugging Face models (pyannote) require accepting their terms and setting `HF_TOKEN`. Pretrained weights are downloaded from their upstream sources and are not redistributed.

## Reproducibility and provenance

The public notebooks preserve the experiments that generated the reported results, and their saved outputs come from the original executions. They were not re-executed after release cleanup.

- **VoxConverse:** notebooks are code-only (Markdown, comments and docstrings removed); executable code is unchanged apart from the path/split-loading cells.
- **Multi-TPC:** each notebook keeps a title cell and short line comments; identifiers and paths were renamed for readability. The comment cleanup did not change the held-out notebook's compiled code, which its frozen-implementation fingerprint checks.

Setup, paths and provenance details are in `docs/VOXCONVERSE_REPRODUCIBILITY.md` and `docs/MULTITPC_REPRODUCIBILITY.md`.

## Data

Dataset audio and annotations are not redistributed in this repository. Obtain VoxConverse and Multi-TPC from their official sources. Configure the VoxConverse paths in each notebook's configuration cell, and set `MULTITPC_ROOT` for the Multi-TPC notebooks (see the two reproducibility documents).

## Paper results

Reported values can be traced to saved outputs in the corresponding notebooks. The exception is the VoxConverse no-augmentation condition: its notebook has no saved outputs, and its results and the paired augmentation bootstrap come from the executed campaign artifacts, which are summarised in `voxconverse_silence_and_diagnostics.ipynb`. Use notebook outputs, not file names or historical development labels, as the source of record.

## Citation

Citation metadata will be added with the final publication record. Until then, please cite the manuscript by title:

> *Leveraging Dual-Process Theory for Multimodal Multiparty Turn-Taking Prediction Using Acoustic and Linguistic Information*
