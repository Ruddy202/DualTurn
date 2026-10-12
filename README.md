# DualTurn

Research code and reproducibility artifacts for:

**Leveraging Dual-Process Theory for Multimodal Multiparty Turn-Taking Prediction Using Acoustic and Linguistic Information**

This repository accompanies work on continuous multiparty turn-taking using a dual-process-inspired computational architecture. A fast candidate-discovery stage proposes plausible transition opportunities, and a selective verification stage evaluates those candidates using complementary contextual evidence.

## Evaluation tasks

The repository separates three evaluation settings:

- **Task A — supplied-point classification:** a decision time is provided and the system predicts SHIFT or HOLD.
- **Task B — automatic-candidate verification:** automatically proposed candidate points are classified as genuine or non-genuine floor transfers.
- **Task C — continuous discovery:** the system discovers, verifies, and localizes floor-transfer events on the continuous interaction timeline.

Task C uses one-to-one temporal event matching, with **±0.50 s** as the primary tolerance and **±0.70 s / ±1.00 s** as sensitivity analyses.

## Datasets

### VoxConverse

VoxConverse is used for the main audio-based experiments. The repository preserves the exact frozen development split used by the executed experiments:

- TRAIN: 177 sessions
- VAL: 39 sessions
- TEST: official VoxConverse TEST partition

The TRAIN and VAL session manifests are provided under `configs/voxconverse/`.

### Multi-TPC

Multi-TPC provides complementary triadic multimodal evidence. The public release will distinguish:

- the original group-disjoint held-out evaluation;
- the post-hoc seven-group nested evaluation; and
- fixed-configuration stage/modality ablations.

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
└── docs/
```

The notebook directories are populated with sanitized copies of the executed research notebooks after release auditing.

## Reproducibility and provenance

The public notebooks are intended to preserve the experiments that generated the reported results. Sanitization is limited to privacy-sensitive paths, notebook metadata, development-only commentary, and public-facing naming where this does not alter computation.

Retained notebook outputs correspond to the original executions. A sanitized notebook is **not** presented as freshly re-executed unless explicitly stated.

The current VoxConverse implementation uses candidate-centred and bounded contextual evidence in several components. The repository therefore documents the executed information contract directly rather than retroactively rewriting the implementation as strictly past-only.

See `docs/VOXCONVERSE_REPRODUCIBILITY.md` for VoxConverse-specific provenance and limitations.

## Data

Dataset audio and annotations are not redistributed in this repository. Users should obtain VoxConverse and Multi-TPC from their respective official sources and arrange them according to the paths documented with each notebook.

## Paper results

The repository will retain the exact executed artifacts used to support the manuscript tables and diagnostic analyses. Numerical values should be traced to the corresponding notebook or frozen result artifact rather than inferred from filenames or development labels.

## Citation

Citation metadata will be added with the final publication record. Until then, please cite the manuscript by title:

> *Leveraging Dual-Process Theory for Multimodal Multiparty Turn-Taking Prediction Using Acoustic and Linguistic Information*

## Release status

Repository assembly is currently being completed on the `public-release` branch. Experimental notebooks are added only after provenance, privacy, and scientific-consistency review.
