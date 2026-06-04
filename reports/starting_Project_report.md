# MoA Prediction Project Plan

## Project Name

**Mechanisms of Action Prediction: Drug Response Multi-Label Classification**

## Project Goal

The goal of this project is to build a complete machine learning pipeline for predicting drug Mechanisms of Action using:

* gene expression features,
* cell viability features,
* treatment metadata,
* feature engineering,
* multi-label classification models,
* model evaluation,
* error analysis,
* and final model improvement.

This project should be professional, clean, and step-by-step. Every notebook should have a clear purpose and should avoid unnecessary repetition.

---

# 1. Full Project Workflow

The project will be completed in five main parts:

```text
1. Data Integration and Dataset Understanding
2. Exploratory Data Analysis
3. Feature Engineering
4. Model Training
5. Model Training 2.0 and Final Model Improvement
```

Each part should produce useful outputs for the next part.

---

# 2. Project Folder Structure

```text
moa-prediction-project/
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── submissions/
│
├── notebooks/
│   ├── 01_data_integration.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   └── 05_model_training_2_0_final_model.ipynb
│
├── src/
│   ├── config.py
│   ├── feature_groups.py
│   ├── preprocessing.py
│   ├── features.py
│   ├── metrics.py
│   ├── validation.py
│   └── modeling.py
│
├── models/
│   ├── baseline/
│   ├── tuned/
│   └── final_ensemble/
│
├── outputs/
│   ├── figures/
│   ├── oof_predictions/
│   ├── feature_importance/
│   └── experiment_logs/
│
├── reports/
│   └── final_project_report.md
│
├── PROJECT_PLAN.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 3. Dataset Files

The raw dataset files should be placed inside:

```text
data/raw/
```

Expected files:

```text
train_features.csv
test_features.csv
train_targets_scored.csv
train_targets_nonscored.csv
train_drug.csv
sample_submission.csv
```

---

# 4. Notebook 01: Data Integration and Dataset Understanding

## File Name

```text
notebooks/01_data_integration.ipynb
```

## Main Goal

Understand the dataset clearly before EDA, feature engineering, or model training.

This notebook should answer:

* What files are available?
* What does each file mean?
* What does each column mean?
* Which table is the main table?
* Which tables are supporting tables?
* How are the files connected?
* Which column should be used for merging?
* Are there duplicate IDs?
* Are there missing values?
* Are there mismatched IDs?
* Is there any possible data leakage risk?

## Main Table

```text
train_features.csv
```

This is the main training input table.

## Test Main Table

```text
test_features.csv
```

This is the main test input table.

## Key Column

```text
sig_id
```

`sig_id` is the unique sample identifier. It is used for merging, but it should not be used as a model feature.

## Important Columns

### Metadata Columns

```text
cp_type
cp_time
cp_dose
```

Meaning:

```text
cp_type  = treatment type
cp_time  = treatment duration
cp_dose  = treatment dose
```

Possible values:

```text
cp_type: trt_cp, ctl_vehicle
cp_time: 24, 48, 72
cp_dose: D1, D2
```

### Gene Expression Features

```text
g-0 to g-771
```

These are gene expression response features.

### Cell Viability Features

```text
c-0 to c-99
```

These are cell viability response features.

### Scored Target Columns

These are the main MoA labels from:

```text
train_targets_scored.csv
```

They are binary columns:

```text
0 = target not active
1 = target active
```

### Non-Scored Target Columns

These are extra auxiliary labels from:

```text
train_targets_nonscored.csv
```

They should not be used in the first baseline model. They may be used later for advanced multi-task learning.

### Drug ID

From:

```text
train_drug.csv
```

Column:

```text
drug_id
```

This can be useful for validation and leakage analysis, but it should not be used blindly as a model feature.

## Data Integration Steps

### Step 1: Load all raw files

Load:

```text
train_features.csv
test_features.csv
train_targets_scored.csv
train_targets_nonscored.csv
train_drug.csv
sample_submission.csv
```

### Step 2: Check shapes

Check row and column counts for every file.

### Step 3: Check duplicate keys

Check whether `sig_id` is unique in each file.

Expected:

```text
train_features["sig_id"].is_unique == True
test_features["sig_id"].is_unique == True
train_targets_scored["sig_id"].is_unique == True
train_targets_nonscored["sig_id"].is_unique == True
train_drug["sig_id"].is_unique == True
sample_submission["sig_id"].is_unique == True
```

### Step 4: Check missing values

Check missing values in every table.

### Step 5: Check ID alignment

Check:

```text
train_features sig_id == train_targets_scored sig_id
train_features sig_id == train_targets_nonscored sig_id
train_features sig_id == train_drug sig_id
test_features sig_id == sample_submission sig_id
```

### Step 6: Merge train features with scored targets

Use:

```text
train_features + train_targets_scored
```

Merge key:

```text
sig_id
```

Merge type:

```text
left merge
```

Reason:

The training feature table is the main table. We want to keep all training samples and attach the scored target labels.

### Step 7: Keep nonscored targets separate

Do not mix nonscored targets with the first baseline.

### Step 8: Keep drug information separate

Use `train_drug.csv` for:

* duplicate drug analysis,
* drug-aware validation,
* leakage checking.

Do not use `drug_id` directly as a normal feature in the first model.

### Step 9: Check control samples

Control samples:

```text
cp_type == "ctl_vehicle"
```

Important rule:

Control samples should have no active MoA target.

Later, during final prediction, test rows with:

```text
cp_type == "ctl_vehicle"
```

should have all target probabilities set to zero.

### Step 10: Save clean interim files

Save outputs to:

```text
data/interim/
```

Expected outputs:

```text
train_features_clean.parquet
test_features_clean.parquet
train_targets_scored_clean.parquet
train_targets_nonscored_clean.parquet
train_drug_clean.parquet
train_main_scored.parquet
feature_groups.json
data_validation_report.json
```

## Notebook 01 Final Summary

At the end of Notebook 01, write a short summary explaining:

* what the main table is,
* what the target table is,
* how the data was merged,
* whether duplicate IDs were found,
* whether missing values were found,
* whether mismatched IDs were found,
* whether control samples follow the expected target behavior,
* and what files were saved for the next step.

---

# 5. Notebook 02: Exploratory Data Analysis

## File Name

```text
notebooks/02_eda.ipynb
```

## Main Goal

Understand the data patterns before feature engineering.

This notebook should not randomly plot everything. Every graph must have a reason.

## Main Sections

```text
1. EDA Objective
2. Load Clean Interim Data
3. Metadata Analysis
4. Target Distribution Analysis
5. Multi-Label Target Behavior
6. Gene Feature Analysis
7. Cell Viability Feature Analysis
8. Treatment-Time-Dose Analysis
9. Target Co-occurrence Analysis
10. PCA Structure Check
11. EDA Findings and Feature Engineering Decisions
```

## Important EDA Questions

### Metadata

* How many treated samples are there?
* How many control samples are there?
* How are `cp_time` values distributed?
* How are `cp_dose` values distributed?
* Is train/test metadata distribution similar?

### Targets

* How many scored targets exist?
* How sparse are the target labels?
* Which targets are most frequent?
* Which targets are rare?
* How many active targets does each sample have?
* Do some targets appear together?

### Gene Features

* What is the distribution of gene expression values?
* Are gene features centered?
* Which gene features have high variance?
* Are there extreme values?

### Cell Viability Features

* What is the distribution of cell viability values?
* Are cell features different from gene features?
* Do cell features capture toxicity-like signals?

### PCA / Structure

* Can PCA separate control and treated samples?
* Can PCA show difference by dose?
* Can PCA show difference by time?

## Recommended Visuals

Use meaningful visuals only:

```text
- cp_type count plot
- cp_time count plot
- cp_dose count plot
- top 30 target frequency plot
- rare target distribution plot
- active target count per sample
- target co-occurrence heatmap
- gene mean/std distribution
- cell mean/std distribution
- PCA scatter by cp_type
- PCA scatter by cp_dose
- PCA scatter by cp_time
```

## EDA Decision Table

At the end, create a decision table:

```text
Finding | Why it matters | Action for feature engineering/modeling
```

Example:

```text
Targets are sparse | Multi-label imbalance problem | Use multilabel stratified CV
Control samples have no active targets | Predicting positive labels for controls is wrong | Apply control post-processing
Gene features are high-dimensional | May contain redundant signals | Try PCA features
Cell features capture treatment effect | Useful biological signal | Keep cell features separately
```

---

# 6. Notebook 03: Feature Engineering

## File Name

```text
notebooks/03_feature_engineering.ipynb
```

## Main Goal

Create clean model-ready features from raw biological features and metadata.

## Main Sections

```text
1. Feature Engineering Objective
2. Load Interim Data
3. Define Feature Groups
4. Encode Metadata Features
5. Scale Numeric Features
6. Create Gene Statistical Features
7. Create Cell Viability Statistical Features
8. Create PCA Features
9. Optional Cross-Group Features
10. Save Processed Datasets
11. Feature Engineering Summary
```

## Feature Groups

### Metadata Features

```text
cp_type
cp_time
cp_dose
```

Feature engineering:

```text
one-hot encoding
```

### Gene Features

```text
g-0 to g-771
```

Possible derived features:

```text
gene_mean
gene_std
gene_min
gene_max
gene_median
gene_abs_mean
gene_positive_count
gene_negative_count
```

### Cell Features

```text
c-0 to c-99
```

Possible derived features:

```text
cell_mean
cell_std
cell_min
cell_max
cell_median
cell_abs_mean
cell_low_signal_count
```

### PCA Features

Create:

```text
gene PCA features
cell PCA features
```

Possible numbers:

```text
50 gene PCA components
20 cell PCA components
```

### Cross-Group Features

Possible features:

```text
gene_cell_mean_difference
gene_cell_std_difference
gene_abs_mean_minus_cell_abs_mean
```

## Important Rule

Feature engineering must be useful and explainable. Do not add complicated features without reason.

## Save Outputs

Save to:

```text
data/processed/
```

Expected outputs:

```text
X_train_base.parquet
X_test_base.parquet
X_train_pca.parquet
X_test_pca.parquet
y_scored.parquet
feature_manifest.json
```

---

# 7. Notebook 04: Model Training

## File Name

```text
notebooks/04_model_training.ipynb
```

## Main Goal

Train clean baseline models and compare them professionally.

## Main Sections

```text
1. Modeling Objective
2. Load Processed Data
3. Define Evaluation Metric
4. Define Validation Strategy
5. Constant Probability Baseline
6. Logistic Regression / Linear Baseline
7. LightGBM / XGBoost Baseline
8. Neural Network Baseline
9. OOF Prediction Saving
10. Model Comparison
11. Error Analysis
12. Initial Submission
```

## Evaluation Metric

Use:

```text
Mean column-wise log loss
```

This is suitable because the problem is multi-label classification and each target prediction is a probability.

## Validation Strategy

Use:

```text
Multilabel Stratified K-Fold
```

Why:

The targets are sparse and imbalanced. Normal random split can create unstable validation results.

Also later test:

```text
GroupKFold by drug_id
```

This is for robustness and leakage analysis.

## Baseline Models

Train models in this order:

```text
1. Constant probability baseline
2. Logistic Regression / Ridge-style baseline
3. LightGBM or XGBoost
4. Simple MLP neural network
```

## Save Outputs

Save to:

```text
outputs/oof_predictions/
outputs/experiment_logs/
models/baseline/
data/submissions/
```

Expected outputs:

```text
baseline_oof_predictions.npy
baseline_test_predictions.npy
experiment_log.csv
initial_submission.csv
```

## Important Rule

Do not repeat the same training code many times.

Create reusable functions for:

```text
metric calculation
fold creation
model training
prediction
OOF saving
experiment logging
```

---

# 8. Notebook 05: Model Training 2.0 and Final Model

## File Name

```text
notebooks/05_model_training_2_0_final_model.ipynb
```

## Main Goal

Fix problems from Model Training 1.0 and build the final improved model.

## Main Sections

```text
1. Review Model Training 1.0 Results
2. Analyze Weak Targets
3. Analyze Rare Targets
4. Analyze Overconfident Predictions
5. Compare Feature Sets
6. Tune Neural Network
7. Seed Averaging
8. Model Blending
9. Control Sample Post-processing
10. Final Submission
11. Final Conclusion
```

## Problems to Check

```text
Which targets have high log loss?
Are rare targets performing badly?
Are predictions too confident?
Does PCA improve performance?
Does LightGBM perform better than neural network?
Does neural network perform better than boosting?
Does ensembling improve CV score?
Are control samples predicted incorrectly?
```

## Final Improvement Ideas

```text
1. Probability clipping
2. Control sample post-processing
3. Seed averaging
4. Model blending
5. Better neural network architecture
6. Target-wise error analysis
7. Rare target analysis
8. Optional auxiliary nonscored target learning
```

## Final Prediction Strategy

Example:

```text
final_prediction =
0.50 * neural_network_seed_average
+ 0.25 * resnet_mlp_seed_average
+ 0.15 * lightgbm_prediction
+ 0.10 * logistic_baseline_prediction
```

Then apply:

```text
control sample post-processing
probability clipping
submission formatting
```

## Save Outputs

Save to:

```text
models/final_ensemble/
outputs/oof_predictions/
outputs/experiment_logs/
data/submissions/
reports/
```

Expected outputs:

```text
final_oof_predictions.npy
final_test_predictions.npy
final_submission.csv
final_experiment_log.csv
final_project_report.md
```

---

# 9. Source Code Plan

## `src/config.py`

Purpose:

Store paths and global settings.

Should include:

```text
ROOT_DIR
RAW_DATA_DIR
INTERIM_DATA_DIR
PROCESSED_DATA_DIR
SUBMISSION_DIR
OUTPUT_DIR
MODEL_DIR
ID_COL
RANDOM_STATE
N_FOLDS
```

## `src/feature_groups.py`

Purpose:

Identify feature groups.

Should include:

```text
metadata features
gene features
cell features
target features
input features
```

## `src/preprocessing.py`

Purpose:

Reusable preprocessing functions.

Should include:

```text
missing value checks
duplicate checks
ID alignment checks
metadata encoding
scaling
```

## `src/features.py`

Purpose:

Reusable feature engineering functions.

Should include:

```text
gene statistical features
cell statistical features
PCA features
cross-group features
feature manifest creation
```

## `src/metrics.py`

Purpose:

Evaluation metrics.

Should include:

```text
mean column-wise log loss
prediction clipping
```

## `src/validation.py`

Purpose:

Cross-validation strategies.

Should include:

```text
multilabel stratified k-fold
group k-fold by drug_id
fold summary checks
```

## `src/modeling.py`

Purpose:

Reusable model training functions.

Should include:

```text
train one fold
run cross-validation
save OOF predictions
save test predictions
log experiment results
```

---

# 10. General Project Rules

## Rule 1: Do not repeat analysis unnecessarily

Each notebook should have a clear purpose.

Bad style:

```text
same missing value check repeated in every notebook
same graph repeated multiple times
same model training code copied again and again
```

Good style:

```text
one clear check
one useful graph
one reusable function
one short explanation
```

## Rule 2: Every important cell needs a short explanation

Each important notebook cell should answer:

```text
What are we doing?
Why are we doing it?
What did we learn?
```

## Rule 3: Keep raw data unchanged

Never edit files inside:

```text
data/raw/
```

Save cleaned or processed files separately.

## Rule 4: Avoid data leakage

Do not:

```text
use target columns as features
fit PCA/scaler on validation fold
use global target encoding
use sample_submission values as information
use drug_id target encoding without CV
```

## Rule 5: Save outputs clearly

Important outputs should be saved in:

```text
data/interim/
data/processed/
outputs/
models/
data/submissions/
reports/
```

## Rule 6: Keep GitHub clean

Do not push large data files or model files to GitHub.

Use `.gitignore` for:

```text
data/raw/
data/interim/
data/processed/
models/
outputs/
.env
kaggle.json
```

---

# 11. Final Project Completion Checklist

## Setup

* [ ] Create GitHub repository
* [ ] Create project folder structure
* [ ] Add `.gitignore`
* [ ] Add `requirements.txt`
* [ ] Add `README.md`
* [ ] Add `PROJECT_PLAN.md`
* [ ] Add initial `src/` files
* [ ] Place raw dataset files in `data/raw/`

## Notebook 01

* [ ] Load all raw files
* [ ] Explain every file
* [ ] Explain every column group
* [ ] Check shapes
* [ ] Check missing values
* [ ] Check duplicate IDs
* [ ] Check ID alignment
* [ ] Check train/test column consistency
* [ ] Check target validity
* [ ] Check control sample behavior
* [ ] Merge train features with scored targets
* [ ] Save interim files
* [ ] Write final integration summary

## Notebook 02

* [ ] Analyze metadata
* [ ] Analyze target distribution
* [ ] Analyze multi-label behavior
* [ ] Analyze gene features
* [ ] Analyze cell features
* [ ] Analyze target co-occurrence
* [ ] Run PCA structure check
* [ ] Create EDA decision table

## Notebook 03

* [ ] Encode metadata
* [ ] Create gene statistical features
* [ ] Create cell statistical features
* [ ] Create PCA features
* [ ] Create optional cross-group features
* [ ] Save processed features
* [ ] Save feature manifest

## Notebook 04

* [ ] Define metric
* [ ] Define validation strategy
* [ ] Train constant baseline
* [ ] Train linear baseline
* [ ] Train boosting baseline
* [ ] Train simple neural network baseline
* [ ] Save OOF predictions
* [ ] Save experiment log
* [ ] Compare models
* [ ] Create initial submission

## Notebook 05

* [ ] Review Model Training 1.0 problems
* [ ] Analyze weak targets
* [ ] Analyze rare targets
* [ ] Tune model
* [ ] Try seed averaging
* [ ] Try model blending
* [ ] Apply control sample post-processing
* [ ] Apply prediction clipping
* [ ] Save final submission
* [ ] Write final conclusion

---

# 12. Immediate Next Step

Start with:

```text
notebooks/01_data_integration.ipynb
```

Do not start EDA yet.

First complete:

```text
data loading
dataset explanation
column explanation
duplicate checks
missing checks
ID matching checks
safe merging plan
interim file saving
```

After Notebook 01 is complete, move to EDA.
