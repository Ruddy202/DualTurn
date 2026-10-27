# Reproducing the Multi-TPC experiments

This guide covers setup, run order and outputs for the three Multi-TPC notebooks. For installation, see the [README](../README.md#installation).

## 1. Data

Multi-TPC is publicly available:

- Dataset (Zenodo): https://doi.org/10.5281/zenodo.17935560
- Authors' code repository: https://github.com/MCMartinLee/Multi-TPC
- Project page: https://mcmartinlee.github.io/projects/MultiTPC

Download and extract the Zenodo archive, then point the notebooks at the extracted root:

```bash
export MULTITPC_ROOT=/absolute/path/to/Multi-TPC
```

The loaders find each session's participant audio, participant-state/gaze/backchannel annotations, word alignments, prosody, motion and gaze streams under this root. They check every stream and stop with a list of missing files if any are absent.

The experiments use 23 complete sessions from seven triadic groups. The loader rejects one motion stream because its duration does not match the session; that stream is not force-aligned.

## 2. Protocols

| Notebook | Protocol | Split |
|---|---|---|
| `multitpc_heldout_evaluation.ipynb` | Group-disjoint held-out | TRAIN `03-04-2022`, `03-05-2022`, `03-11-2022`, `03-12-2022`, `12-15-2021`; VAL `02-11-2022`; TEST `01-28-2022` |
| `multitpc_seven_group_evaluation.ipynb` | Seven-group nested | Each group is the outer TEST group once; models and settings are selected on the other six |
| `multitpc_ablation.ipynb` | Fixed-configuration ablation | Same outer folds as the seven-group protocol |

The seven-group and ablation notebooks evaluate a revised system developed after the held-out evaluation. The proposed system's text branch is disabled in that configuration.

Ablation conditions: full system, Stage 1 only, audio only, minus gaze, minus motion, minus prosody, minus WavLM, minus ECAPA. The full-system settings are selected once and held fixed for every condition.

## 3. Configuration

| Variable | Default | Used by | Purpose |
|---|---|---|---|
| `MULTITPC_ROOT` | — (required) | all | Corpus root; runs are written under `$MULTITPC_ROOT/runs/` |
| `MUVAP_REPO` | `third_party/muvap/MuVAP-main` | held-out, seven-group | MuVAP source |
| `MUVAP_ROLE_VAP_RELEASE` | downloaded | held-out, seven-group | Local folder with MuVAP role-VAP `weights.pt` and `config.yaml`; otherwise downloaded from the Hugging Face repository `Haotian-Qi/MuVAP` |
| `MULTITPC_COMPARATOR_FREEZE` | see section 5 | held-out | Comparator freeze bundle |
| `MULTITPC_SEVEN_GROUP_RUN_DIR` | searched under `runs/multitpc_seven_group_nested/` | ablation | Seven-group run whose full-system selection is reused; used only if its protocol, data and code fingerprints match |
| `MULTITPC_SHARED_AUDIO_CACHE` | seven-group cache | ablation | Shared WavLM/ECAPA feature cache |
| `MULTITPC_SHARED_CAUSAL_CACHE` | seven-group cache | ablation | Shared causal feature cache |
| `CUDA_MIN_FREE_GB_FOR_MAIN` | `4.0` | all | Minimum free GPU memory before a stage falls back to CPU |
| `FORCE_MAIN_CPU` | `0` | all | Run the main models on CPU |

## 4. Run order and outputs

| Step | Notebook | Writes to `$MULTITPC_ROOT/runs/` | Runtime |
|---|---|---|---|
| 1 | `multitpc_seven_group_evaluation.ipynb` | `multitpc_seven_group_nested/` | Several days on one GPU |
| 2 | `multitpc_ablation.ipynb` | `multitpc_fixed_configuration_ablation/` | Shorter when step 1 caches exist |
| — | `multitpc_heldout_evaluation.ipynb` | `MultiTPC_MASTER_R11_TASKABC_AUX_AUDIO_V7/` | Needs the frozen artifacts in section 5 |

Steps 1 and 2 start from the raw corpus and need no other inputs. If step 1 has not been run, the ablation notebook first repeats the nested selection for the full system.

The seven-group and ablation notebooks hash their own source code into the run-directory name. A fresh run writes to a new directory and does not reuse caches from an earlier run.

## 5. Frozen artifacts for the held-out evaluation

The held-out notebook does not train the proposed system. It loads the models and comparator settings frozen during development, checks their SHA-256 hashes and code fingerprints, and scores the TEST group once. These files are not included in this repository. Without them, the notebook stops before scoring.

The frozen held-out model files are available from the authors on request. Retraining replacements for them would be a new experiment, not a reproduction of the reported result; the seven-group and ablation notebooks run without them.

Expected locations, relative to `$MULTITPC_ROOT/runs/MultiTPC_MASTER_R11_TASKABC_AUX_AUDIO_V7/`:

| File | Contents |
|---|---|
| `protected_r10_1_baseline/development/r10_development_status.json` | Selected candidate-proposal operating point |
| `protected_r10_1_baseline/models/r10_candidate_meta_models.pkl` | Candidate-proposal models |
| `protected_r10_1_baseline/models/r10_activity_full.pt` | Voice-activity model |
| `protected_r10_1_baseline/models/r10_fap_full.pt` | Future-activity model |
| `development/r11_frozen_settings.json`, `development/r11_development_status.json` | Frozen proposed-system settings |
| `models/r11_models.pkl` | Proposed-system verifier |
| `results/r11_branch_comparison.csv`, `results/r11v5_task{A,B,C}_*.csv` | Development results checked before TEST |
| `comparators_final_v1/models/comparator_locked_freeze.pkl` and `.json` | Frozen comparator bundle and manifest |
| `comparators_final_v1/models/lee24_automatic_causal_development.pkl` | Lee et al. (2024) comparator |
| `comparators_final_v1/models/triadic_vap_development_paper_constrained.pt` | Triadic VAP comparator |
| `comparators_final_v1/models/muvap_multitpc_fusion.pt` | MuVAP comparator |

`r11_frozen_settings.json` stores the absolute paths of the model files. Place the artifacts at the same absolute location as in the original run, or the path check fails.

## 6. Evaluation settings

- Candidates are labelled, and operating points are selected, with a ±1.00 s matching tolerance (`PRIMARY_EVENT_TOLERANCE = 1.0`).
- Task C is reported at ±0.50 s, ±0.70 s and ±1.00 s with one-to-one matching.
- Reference SHIFT events are normal turn transfers (NTT) and interruption turn transfers (ITT).
- The seven-group and ablation analyses use 10,000 bootstrap replicates and Holm correction for paired comparisons.

## 7. Information available at prediction time

The proposed system is causal. WavLM and ECAPA windows end at the candidate time, and System 1 picks candidates with causal peak picking.

## 8. Models

| Model | Source |
|---|---|
| WavLM | `microsoft/wavlm-large`, revision `c1423ed94bb01d80a3f5ce5bc39f6026a0f4828c` |
| Speaker embeddings | `speechbrain/spkrec-ecapa-voxceleb` |
| MuVAP | Source in `third_party/muvap/MuVAP-main/` (commit `a1ef9c8`); role-VAP weights (`vap-role-cpc`) from the Hugging Face repository `Haotian-Qi/MuVAP` |

## 9. Names in the held-out notebook

The held-out notebook keeps internal prefixes because they appear in its frozen-artifact filenames and code fingerprint:

- `R10_*`: candidate-proposal stack;
- `R11_*`: proposed held-out system;
- `V17_*`: shared timeline, voice-activity and future-activity code.

## 10. Hardware

All experiments ran on a single consumer GPU with 12–16 GB of memory, using Python 3.11.15 and PyTorch 2.7.0+cu118.
