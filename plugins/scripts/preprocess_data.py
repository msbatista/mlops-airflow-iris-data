from ctypes import Union
import os
import pandas as pd
from typing import List


def categorise_data(row) -> str:
    # TODO: Improve this code to use a dictionary that returns lambda for each property.
    if row['sepal_length'] < 4.3 or row['sepal_length'] > 7.9:
        return 'sepal_length must be within (4.3, 7.9) range.'
    elif row['sepal_width'] < 1.0 or row['sepal_width'] > 4.4:
        return 'sepal_width must be within (1.0, 4.4) range.'
    elif row['petal_length'] < 1.0 or row['petal_length'] > 6.9:
        return 'petal_length must be within (1.0, 6.9) range.'
    elif row['petal_width'] < 0.1 or row['petal_width'] > 2.5:
        return 'petal_length must be within (0.1, 2.5) range.'
    elif row['classEncoder'] not in [0, 1, 2]:
        return 'classEncoder must assume one of the values: 0, 1, 2'
    elif row['class'] not in ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']:
        return "class must assume one of the values: 'Iris-setosa', 'Iris-versicolor' ou 'Iris-virginica'"
    else:
        return None


def load_data(file: str) -> pd.DataFrame:
    return pd.read_csv(file, header=0, index_col=False)


def write_data(file: str, df: pd.DataFrame, sep: str = ',') -> None:
    df.to_csv(file, sep=sep)


def clean_data(df: pd.DataFrame, returnBadResults=True) -> Union[pd.DataFrame, pd.DataFrame]:
    # TODO: Define the valid data range into dictionary so that if it is need to changed the task will be performed only in one place. 
    # TODO: Maybe use pandas schema too to simplify the code.
    cleaned_data_df = df[
        (df['sepal_length'].between(4.3, 7.9)) &
        (df['sepal_width'].between(1.0, 4.4)) &
        (df['petal_length'].between(1.0, 6.9)) &
        (df['petal_width'].between(0.1, 2.5)) &
        (df['classEncoder'].isin([0, 1, 2])) &
        (df['class'].isin(['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']))
    ]

    non_conformant_df = pd.DataFrame()

    if returnBadResults:
        non_conformant_df = df[~df.apply(tuple, 1).isin(
            cleaned_data_df.apply(tuple, 1))]
        non_conformant_df.loc[:, 'messageError'] = non_conformant_df.apply(
            lambda row: categorise_data(row), axis=1)

        return (cleaned_data_df, non_conformant_df)

    return (cleaned_data_df, non_conformant_df)


def main() -> None:
    DATA_DIR = '../data'
    RAW_DATASET = 'raw/iris.txt'
    CLEANED_DATASET = 'processed/cleaned.csv'
    NON_COMPLIANT_DATASET = 'processed/non_compliant.csv'

    file = os.path.join(DATA_DIR, RAW_DATASET)

    df_iris = load_data(file)

    cleaned_df, non_conformant_df = clean_data(
        df=df_iris, returnBadResults=True)

    write_data(file=os.path.join(DATA_DIR, CLEANED_DATASET), df=cleaned_df)
    write_data(file=os.path.join(
        DATA_DIR, NON_COMPLIANT_DATASET), df=non_conformant_df)
