# International Repositories Analysis

## Install requirements

It is recommended to install dependencies in a virtual environment:

`python -m venv venv`
`source venv/bin/activate`

Then install requirements using pip:

`pip install -r requirements.txt`

## Build the dataset

To build the dataset, run `international_opendoar.py`.  This will output raw data in csv format to `data/raw_opendoar_data.csv`.  Data cleaning functions then run and return a cleaned version to `data/cleaned_opendoar_data.csv`.

## Run data analyses

To run the notebook, you must have Jupyter installed (https://jupyter.org/).  From the project folder, open a terminal and run `jupyter lab`.  Click the `international_repos_analysis.ipynb` to run the notebook. This contains descriptions of each analysis and the ability to run each.
