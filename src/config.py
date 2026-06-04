
from pathlib import Path

# Root directory
ROOT_DIR = Path(__file__).resolve().parents[1]

# Data directories
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SUBMISSION_DIR = DATA_DIR / "submissions"

# Output directories
OUTPUT_DIR = ROOT_DIR / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"
OOF_DIR = OUTPUT_DIR / "oof_predictions"
FEATURE_IMPORTANCE_DIR = OUTPUT_DIR / "feature_importance"
EXPERIMENT_LOG_DIR = OUTPUT_DIR / "experiment_logs"

# Model directories
MODEL_DIR = ROOT_DIR / "models"
BASELINE_MODEL_DIR = MODEL_DIR / "baseline"
TUNED_MODEL_DIR = MODEL_DIR / "tuned"
FINAL_MODEL_DIR = MODEL_DIR / "final_ensemble"

# Project settings
ID_COL = "sig_id"
RANDOM_STATE = 42
N_FOLDS = 5
