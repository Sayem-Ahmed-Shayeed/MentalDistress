# MentalDistress reproducibility files

## File structure

```text
MentalDistress/
├── README.md
├── 01_DATA/
│   ├── MentalDistress.csv
│   ├── MentalDistress_train_LOCKED.csv
│   ├── MentalDistress_validation_LOCKED.csv
│   ├── MentalDistress_test_LOCKED.csv
│   └── prepare_locked_splits.py
├── 02_EXPERIMENTS/
│   ├── step02_step03_classical_baselines/
│   ├── step04_transformer_baselines/
│   ├── phase03_phase04_boundary_analysis/
│   ├── phase05_bootstrap_stability/
│   ├── phase06_others_sensitivity/
│   ├── phase08_pair_specialists/
│   ├── phase09_routing_calibration/
│   ├── phase10_controls_allocation/
│   ├── phase11_mechanism_robustness/
│   ├── phase12_efficiency/
│   ├── phase14_locked_test/
│   ├── phase15_external_validation/
│   └── phase16_evidence_consolidation/
└── 03_FINAL_EVIDENCE/
```

Each experiment directory contains the executed notebook and its frozen result ZIP. `03_FINAL_EVIDENCE` contains the extracted final tables, figures, protocols, and evidence summaries.

## Run order

1. `step02_step03_classical_baselines`
2. `step04_transformer_baselines`
3. `phase03_phase04_boundary_analysis`
4. `phase05_bootstrap_stability`
5. `phase06_others_sensitivity`
6. `phase08_pair_specialists`
7. `phase09_routing_calibration`
8. `phase10_controls_allocation`
9. `phase11_mechanism_robustness`
10. `phase12_efficiency`
11. `phase14_locked_test`
12. `phase15_external_validation`
13. `phase16_evidence_consolidation`

Phases 7 and 13 were not used in the final workflow.

## Data

The internal notebooks use the four CSV files in `01_DATA`. Verify or regenerate the exact locked splits with:

```bash
python 01_DATA/prepare_locked_splits.py --verify-only
python 01_DATA/prepare_locked_splits.py
```

For the classical notebook, set:

```bash
export MENTALDISTRESS_DATA_DIR=/absolute/path/to/01_DATA
```

Transformer notebooks retain their original Kaggle paths. Point their initial train, validation, and test path variables to the corresponding files in `01_DATA` when running outside Kaggle.

Phase 15 requires two external datasets that are not included:

- SDCNL: Kaggle dataset `bymahmud/sdcnl-dataset`, file `combined-set.csv`.
- Depression Reddit: Kaggle dataset `infamouscoder/depression-reddit-cleaned`, file `depression_dataset_reddit_cleaned.csv`.

## Environments and versions

### Classical baselines

- Python 3.13.5
- NumPy 2.3.5
- pandas 2.2.3
- SciPy 1.17.0
- scikit-learn 1.8.0
- joblib 1.5.3
- Matplotlib 3.10.8
- threadpoolctl 3.6.0

### Controlled GPU efficiency run

- Python 3.12.13
- NVIDIA Tesla T4
- CUDA 12.8
- PyTorch 2.10.0+cu128
- Transformers 5.0.0
- FP32 inference

Other required Python packages are `numpy`, `pandas`, `scipy`, `scikit-learn`, `matplotlib`, `safetensors`, `joblib`, `threadpoolctl`, `nbformat`, and Jupyter.

The transformer notebooks download these pretrained models:

- `google-bert/bert-base-uncased`
- `FacebookAI/roberta-base`
- `google/electra-base-discriminator`
- `mental/mental-roberta-base`

A CUDA-capable GPU and network access to the pretrained models are required for full transformer retraining.
