# Multi-TPC reproducibility

This page contains the practical setup needed to run the Multi-TPC notebooks in this repository.

## Released notebooks

```text
notebooks/multitpc/
├── multitpc_heldout_evaluation.ipynb
├── multitpc_seven_group_evaluation.ipynb
└── multitpc_ablation.ipynb
```

- `multitpc_heldout_evaluation.ipynb` — original 5/1/1 group-disjoint held-out evaluation.
- `multitpc_seven_group_evaluation.ipynb` — seven-group nested evaluation, with each group used once as the outer held-out group.
- `multitpc_ablation.ipynb` — fixed-configuration stage/modality ablations under the seven-group protocol.

## Dataset acquisition

The official Multi-TPC dataset is publicly available from Zenodo:

- Dataset: https://doi.org/10.5281/zenodo.17935560
- Official project/code repository: https://github.com/MCMartinLee/Multi-TPC
- Project page: https://mcmartinlee.github.io/projects/MultiTPC

Download and extract the Zenodo dataset, then point the notebooks to the extracted dataset root:

```bash
export MULTITPC_ROOT=/absolute/path/to/Multi-TPC
```

The official repository also contains the dataset authors' preprocessing and analysis code for the audio, motion, gaze, and related streams.

## Dataset setup

The notebooks discover the dataset streams used by the experiment, including audio, participant-state/gaze/backchannel annotations, word alignment, prosody, motion, and gaze data.

The audited dataset copy used for the experiments contains **23 complete sessions across seven conversation groups**. One motion stream with a large duration mismatch is rejected by the loader rather than force-aligned.

## Original held-out split

The original held-out notebook uses the frozen group split:

- TRAIN: `03-04-2022`, `03-05-2022`, `03-11-2022`, `03-12-2022`, `12-15-2021`
- VAL: `02-11-2022`
- TEST: `01-28-2022`

The held-out notebook restores the frozen model/comparator artifacts used by the executed experiment. To rerun it, place those artifacts under the run directory configured in the notebook; it is not a training notebook.

It also requires `comparator_locked_freeze.pkl` and its JSON manifest, exported from the completed development kernel before TEST was opened. The notebook stops early if they are missing and cannot recreate them, because that would mean refitting a development-selected object.

## Seven-group evaluation

The seven-group notebook performs group-nested fitting/evaluation directly. Each group is held out once as the outer evaluation group while model/configuration selection uses only the remaining groups.

This is a separate protocol from the original single held-out experiment. It evaluates the later proposed Multi-TPC system, so its results are not repeated evaluations of the frozen held-out model.

## Ablations

The ablation notebook evaluates:

- full configuration;
- Stage-1 only;
- audio only;
- minus gaze;
- minus motion;
- minus prosody;
- minus WavLM;
- minus ECAPA.

The full-configuration hyperparameters are selected first and then held fixed for the ablation comparisons. If the seven-group notebook has been run, its verified full-model selection and caches are reused; otherwise the ablation notebook reruns full-only nested selection.

## Event evaluation

Task C uses one-to-one event matching at:

- ±0.50 s
- ±0.70 s
- ±1.00 s

The event construction distinguishes normal turn transfers (NTT) and interruption turn transfers (ITT).

## Causal input contract

The proposed Multi-TPC pipeline uses information available up to the decision/candidate time. WavLM/ECAPA audio intervals end at the candidate time, automatic candidate generation uses causal peak picking, and the proposed text branch is disabled in the released seven-group configuration.

## Pretrained resources

The notebooks use:

- WavLM Large: `microsoft/wavlm-large`
- WavLM revision: `c1423ed94bb01d80a3f5ce5bc39f6026a0f4828c`
- ECAPA-TDNN: `speechbrain/spkrec-ecapa-voxceleb`

Model weights are downloaded from their upstream sources and are not redistributed here.

## MuVAP dependency

The exact MuVAP source used by the executed experiments is vendored under:

```text
third_party/muvap/MuVAP-main/
```

The upstream MIT licence is retained with the vendored source.

## Running the notebooks

Set `MULTITPC_ROOT`, keep the vendored MuVAP source at `third_party/muvap/MuVAP-main/` (or set `MUVAP_SOURCE_DIR`), restart the kernel, and run each notebook from the top.

## Naming used in the public notebooks

The seven-group and ablation notebooks use descriptive names (`PROPOSER_*`, `PROPOSED_*`, `WAVLM_MODEL_ID`, `STAGE1_MODEL_CONFIGS`, `SESSION_TABLES`, `CausalAudioFeatureAdapter`, `METHOD_FULL`, etc.). `R12_*` strings remain only as cache/result keys of the executed run.

The held-out notebook keeps its internal prefixes because they are part of the frozen-implementation fingerprint and artifact filenames:

- `R10_*` — frozen candidate-proposal stack;
- `R11_*` — frozen proposed held-out system;
- `V17_*` — shared timeline, activity and future-activity support code.

These are compatibility identifiers, not alternative methods.

## Execution note

The notebooks retain scientific outputs from their original executions and were not re-executed after public-release refactoring. The refactor changes naming, paths, comments, and presentation only; it does not redesign the experiment or alter retained numerical results.

The final comment cleanup left the held-out notebook's compiled code unchanged, so its frozen-implementation fingerprint still matches. The seven-group and ablation notebooks hash function source text into their run fingerprint, so a re-run creates a new run directory instead of reusing caches from the executed run.
