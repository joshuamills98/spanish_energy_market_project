# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import pandas as pd


def resample_dataframe(df):
    df = df.resample('1d').mean()
    return df


def drop_absent_cols(df):
    df = df.fillna(0)
    drop_col_list = []
    for col in df.columns:
        if all(df[col] == 0.0):  # If all values are 0
            drop_col_list.append(col)
            print('dropping column: ', col)
    df = df.drop(drop_col_list, axis=1)
    return df


def datetime_conversion(df):
    df.index = pd.to_datetime(df.time, utc=True)
    df = df.drop('time', axis=1)
    return df


@click.command()
@click.argument('input_filename', type=click.Path(exists=True))
@click.argument('output_filename', type=click.Path(exists=True))
def main(input_filename, output_filename):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    logger.info('first input raw data')
    df = pd.read_csv(input_filename)
    print('pk')
    logger.info('Step 1')

    df.to_csv(output_filename)    

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
