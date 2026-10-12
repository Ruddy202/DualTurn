# VoxConverse reproducibility notes

## Purpose

This document records the provenance and reproducibility contract for the VoxConverse artifacts released with this repository.

The public notebooks are sanitized copies of executed research notebooks. Their role is to expose the experiment that produced the retained results, not to replace it with a newly redesigned experiment.

## Frozen development split

The executed VoxConverse experiments use:

- TRAIN: 177 sessions
- VAL: 39 sessions
- TEST: the official VoxConverse TEST partition discovered from the dataset files

The exact development manifests are distributed as:

```text
configs/voxconverse/train_sessions.json
configs/voxconverse/val_sessions.json
```

TRAIN and VAL are disjoint and together contain 216 DEV sessions.

The original experiment did not use a separate `test_sessions.json`; the public release therefore does not introduce one.

Public notebooks should fail clearly when the frozen TRAIN/VAL manifests are missing rather than silently create a replacement split.

## Public-notebook provenance

For each released notebook:

- scientific code and retained numerical outputs originate from the executed research artifact;
- notebooks are not re-executed merely for sanitization;
- privacy-sensitive filesystem paths and machine-specific metadata may be removed or replaced;
- development-history comments and reader-facing labels may be shortened or clarified only when computation is unchanged;
- no output should be fabricated to make a sanitized notebook appear freshly executed.

A short provenance notice should appear near the beginning of each public notebook.

## Information contract

The executed VoxConverse pipeline contains bounded look-ahead/context in several components. Examples identified during the source audit include:

- candidate-centred WavLM windows;
- right-side ASR context used by Qwen-derived scores;
- post-candidate acoustic, diarization, ASR, and speaker-comparison features in some System-2 routes;
- symmetric neighbouring-candidate context for temporal verification;
- post-candidate evidence in RR-FAP diagnostics.

These behaviours are properties of the executed experiment and are preserved in the public research artifacts. Public documentation should not describe those routes as strictly past-only unless a separate re-executed causal experiment is provided.

No direct TEST ground-truth label leakage into the final TEST feature/prediction path was identified in the source audit.

## Task mapping

Legacy development labels map to the public task terminology as follows:

- Branch 2 -> Task A: supplied-point SHIFT/HOLD classification
- Branch 2E -> Task B: automatic-candidate verification
- Branch 1 -> Task C: continuous discovery
- Branch 3 -> future-activity diagnostic

Blind string replacement must not be used because Branch 2E is scientifically distinct from Branch 2.

## Canonical TEST reference

The final Task-C evaluation canonicalizes raw SHIFT rows to unique session-time events.

- raw TEST SHIFT rows: 6,350
- canonical TEST SHIFT events: 6,348

Final Task-C event metrics use the 6,348-event canonical reference.

## Primary Task-C matching tolerances

- primary: ±0.50 s
- sensitivity: ±0.70 s
- sensitivity: ±1.00 s

Matching is one-to-one.

## Augmentation terminology

The executed waveform-augmentation condition may include:

- random gain;
- Gaussian noise; and
- optional background/diffusion-bed mixing.

The executed campaign explicitly does not use speed perturbation or temporal shifting.

For public naming, `waveform_augmentation` is preferred over the legacy `diffusion_only` label because it more accurately describes the actual executed condition.

The main evaluation notebook already represents the full augmentation condition; a redundant public `full` ablation notebook is unnecessary unless it contains unique reproducibility evidence.

## Final-route interpretation

The original main/full TEST configuration selects a weighted ranker + temporal route with local timing correction.

RR-FAP and the meta-confirmer are evaluated component/alternative routes but are not used by the headline final Task-C rule in the original main/full execution.

## Bootstrap provenance

The original main Task-C confidence interval was generated with 1,000 session-level bootstrap replicates.

The augmentation comparison separately used 2,000 paired session-level bootstrap replicates.

These should not be conflated in the public release.

## Human audit

A 300-event human-review package was prepared, but the retained analysis reports 0/300 items reviewed. The manual event-label audit therefore remains incomplete.

## Cache provenance

The original development notebook contains instances where existing temporal caches were loaded despite metadata mismatch. This is a limitation of the historical execution and should not be erased from provenance.

Sanitization may remove noisy cache logs, but must not imply that the retained historical outputs were produced under a stricter cache-validation policy than was actually used.

## Runtime interpretation

Reported runtime values are component-level measurements. They do not constitute an end-to-end real-time benchmark including diarization, ASR, embedding extraction, language-model processing, and all feature computation.

## Data redistribution

VoxConverse audio and annotation files are not redistributed here. Users must obtain the dataset from its official source.
