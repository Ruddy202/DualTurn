# VoxConverse public-release audit

## Verdict

**GREEN for public release as a faithful, sanitized record of the executed VoxConverse experiments.**

This verdict concerns repository publication of the historical executed artifacts. It does **not** convert the executed pipeline into a strictly causal/past-only system. The public notebooks disclose that bounded look-ahead/context is present in the historical implementation.

## Files verified

- `voxconverse_main_evaluation.ipynb`
- `voxconverse_ablation_no_augmentation.ipynb`
- `voxconverse_ablation_synthetic_only.ipynb`
- `voxconverse_ablation_waveform_augmentation.ipynb`
- `voxconverse_silence_and_diagnostics.ipynb`

The cleaned notebooks were compared against the corresponding original notebooks supplied with the project.

## Scientific-equivalence check

For the main and three augmentation notebooks, the only executable-code change is the public path/split-loading cell: personal filesystem defaults were replaced by repository-relative/environment-configurable paths, the exact frozen TRAIN/VAL manifests are required, and silent split regeneration is disabled.

All other code cells are unchanged relative to the corresponding original source notebook.

For the silence/diagnostics notebook, the only executable-code change is the path/configuration cell used to resolve repository-relative data and result locations. All analysis code cells are otherwise unchanged.

The notebooks were not re-executed after sanitization.

## Frozen split

- TRAIN: 177 unique sessions
- VAL: 39 unique sessions
- TRAIN/VAL overlap: 0

No `test_sessions.json` is introduced because the original experiment discovers the official VoxConverse TEST partition from the dataset files.

## Output provenance

Scientifically useful saved outputs are retained. Progress bars, repeated warnings, tracebacks, and personal/machine-specific path output were reduced or sanitized.

A numerical-token comparison found no numerical values newly introduced into retained outputs by sanitization.

Key retained anchors include:

- Task A Macro-F1 ≈ 0.848836; SHIFT F1 ≈ 0.865545
- Task B F1 ≈ 0.455280
- Task C @ ±0.50 s: P = 0.536176, R = 0.568526, F1 = 0.551877
- TP = 3609, FP = 3122, FN = 2739, N_pred = 6731, N_gt = 6348
- Task C @ ±0.70 s F1 ≈ 0.597
- Task C @ ±1.00 s F1 ≈ 0.620
- System-1 TEST candidates ≈ 80,012
- candidate ceiling ≈ 6092 / 6348
- synthetic-only augmentation F1 ≈ 0.5495
- waveform-augmentation condition F1 ≈ 0.5424
- pure automatic silence F1 ≈ 0.1959
- silence + automatic speaker change F1 ≈ 0.3417
- System-1 component RTF ≈ 0.232
- temporal-verifier latency ≈ 0.011286 ms/candidate
- manual event-label audit status: 0/300 reviewed

The no-augmentation source notebook contains no saved outputs. The public copy preserves that fact and does not fabricate output cells; aggregate no-augmentation results are supported by the executed campaign artifacts.

## Terminology

Public task mapping:

- original Branch 2 -> Task A
- original Branch 2E -> Task B
- original Branch 1 -> Task C
- original Branch 3 -> future-activity diagnostic

Legacy internal artifact keys may remain where changing them would risk provenance or artifact lookup.

The public `waveform_augmentation` notebook corresponds to the original `diffusion_only` condition. The executed condition uses timing-preserving random gain, Gaussian noise, and optional background/diffusion-bed mixing; it does not use speed perturbation or temporal shifting.

The main evaluation is the full augmentation condition, so a redundant public full-condition notebook is unnecessary.

## Information-contract disclosure

The original executed VoxConverse pipeline contains bounded look-ahead/context in several components. The public notebooks preserve this historical implementation and must not be represented as a newly re-executed strictly causal pipeline.

No direct TEST ground-truth-label leakage into the final TEST feature/prediction path was identified in the source audit.

## Bootstrap provenance

The original main Task-C confidence interval uses 1,000 session-level bootstrap replicates. The augmentation comparison separately uses 2,000 paired session-level bootstrap replicates. The release preserves this distinction.

## Privacy and integrity

A final scan over notebook source, Markdown, outputs, and metadata found no personal filesystem paths, local username, email addresses, private IPv4 addresses, or common credential/token patterns.

All five notebooks parse as valid notebook JSON and all Python code cells compile syntactically.

## Remaining limitations

- Historical internal run identifiers remain in some cache/artifact names and retained outputs.
- Historical cache-resume behavior included cases where temporal caches were loaded despite metadata mismatch.
- The human 300-event audit remains incomplete.
- Runtime figures are component-level, not whole-pipeline uncached real-time measurements.
- The main Task-C bootstrap and augmentation bootstrap use different replicate counts.
- The release documents the executed bounded-context pipeline rather than claiming strict past-only causality.

## Recommendation

**SAFE TO PUBLISH on the repository review branch as executed-artifact evidence**, provided the README/manuscript preserve the information-contract and provenance distinctions above.
