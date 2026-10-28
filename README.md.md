# Explainable Machine Learning for Automated Quality Control of scRNA-seq Data

Code for the manuscript *"Explainable Machine Learning for Automated Quality Control of Single-Cell RNA-seq Data Across Independent PBMC Datasets"*.

## Summary
Quality control (QC) of single-cell RNA-seq data usually relies on fixed thresholds that are chosen by hand and are hard to apply the same way across datasets. In this project, machine-learning models were trained to reproduce a predefined QC rule (200 < detected genes < 6,000 and mitochondrial fraction < 15%) on three public PBMC datasets, and SHAP and feature ablation were used to see which features the models rely on. Doublets were then removed, cell types were annotated and marker genes were checked to confirm that the retained cells form biologically sensible populations. The aim is a fast, explainable way to apply a stated QC policy consistently.

## Pipeline steps
1. Quality control: compute per-cell metrics (genes, counts, mitochondrial, ribosomal and haemoglobin fractions) and assign rule-derived Good/Bad labels
2. Doublet removal with Scrublet
3. Normalisation, highly variable genes, PCA, UMAP and Leiden clustering
4. Cell-type annotation with CellTypist, plus Wilcoxon marker genes and Enrichr enrichment
5. Model training: Random Forest, XGBoost and a neural network on seven engineered features
6. Model explanation with SHAP and feature ablation
7. Cross-dataset validation: train on two datasets, test on the third

## Key results
| Dataset | Best model | F1 (Good) | AUC |
|---|---|---|---|
| A (3k PBMC) | XGBoost | 0.985 | 0.996 |
| B (10k PBMC, 5' v2) | XGBoost | 0.997 | 0.999 |
| C (10k PBMC) | XGBoost | 0.992 | 0.999 |

Leave-one-dataset-out validation with unscaled features gave F1 of 0.988 (test A), 0.999 (test B) and 0.984 (test C). Standardising features within each dataset reduced transfer sharply, because the QC rule uses absolute thresholds.

## Important caveat
The models reproduce a predefined QC rule. They do not identify biologically "true" good cells, and the labelling variables can largely be recovered from the input features. High accuracy therefore shows that the rule can be approximated, not that the models detect cell viability.

## Datasets
All data are public datasets from 10x Genomics, available at https://www.10xgenomics.com/datasets. The raw data are not included in this repository. Search for each title or file name below, download the file, and set `DATA_PATH` at the top of the notebook to its location.

| Dataset | Description | File used | Notebook |
|---|---|---|---|
| A | PBMC from a Healthy Donor - No Cell Sorting (3k), Multiome gene expression | `pbmc_unsorted_3k_filtered_feature_bc_matrix.h5` | `AI_Powered_scRNAseq_Corrected_Pipeline.ipynb` |
| B | 10k human PBMC, 5' v2 multi | `sc5p_v2_hs_PBMC_10k_multi_5gex_5fb_b_t_count_filtered_feature_bc_matrix.h5` | `AI-powered dataset 2.ipynb` |
| C | PBMC from a Healthy Donor - No Cell Sorting (10k), Multiome gene expression (raw matrix) | `pbmc_unsorted_10k_raw_feature_bc_matrix.h5` | `aipowered.2.01 (1).ipynb` |

Dataset pages on 10x Genomics may have several versions, and file sizes can differ slightly between versions.

## How to run
1. `pip install -r requirements.txt`
2. Run each notebook from top to bottom. The last cell saves `features_A.csv`, `features_B.csv` or `features_C.csv` (these files are included here).
3. Put the three CSV files and `cross_dataset_validation_standalone.py` in one folder and run `python cross_dataset_validation_standalone.py` for leave-one-dataset-out validation.

## Outputs
Marker genes, model comparison, feature importance, feature ablation results and cross-dataset results are saved as CSV files by the notebooks and the script.

## Citation
[Add the preprint DOI here once available.]

## Licence
MIT (see `LICENSE`).
