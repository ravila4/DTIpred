# DTIpred

Machine learning models for predicting drug-target interactions (DTIs) and other properties.

## Project Organization

    ├── LICENSE
    ├── README.md
    ├── data
    │   ├── 01_pharos_raw_data
    │   ├── 02_receptor_ids
    │   ├── 03_ligand_smiles
    │   ├── 04_sequences
    │   ├── 05_mol2vec     <- Featurized ligand data
    │   └── 06_prot2vec    <- Featurized protein data
    │
    ├── models             <- Trained models.
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── references         <- Relevant publications and bibliography materials.
    │
    ├── reports            <- Generated analysis PDF and LaTeX. PDFs for Jupyter notebooks.
    │   └── figures        <- Graphics and figures.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment.
    │
    ├── setup.py           <- Makes project pip installable (pip install -e .) so src can be imported.
    │
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data.
        │   ├── fetch_chembl.py
        │   └── get_sequences.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │   │                 predictions
        │   ├── predict_model.py
        │   └── train_model.py
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
