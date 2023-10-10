import logging
import os

import pandas as pd
from src.utils import config
#from src.utils.connect import DatabaseModelsClass
#from dotenv import find_dotenv, load_dotenv
#import requests


class GetDataTemplate:
    """ Class to etl data. """
    logger = logging.getLogger(f"{__name__}.GetDataTemplate")
    #database_instance = DatabaseModelsClass('MYSQLLINUX')

    #load_dotenv(find_dotenv())
    #APIKEY = os.environ.get('KEYNAME')
    DATA_FOLDER = os.path.join(config.ROOTDIR, 'data')

    def get_excel_WELLMUM(self):
        self.logger.debug(f"- get_excel_WELLMUM")

        path = os.path.join(self.DATA_FOLDER, 'raw', 'WELLMUM_20231008_v0.2.xlsx')
        df_import = pd.read_excel(path, 'Sheet2', engine='openpyxl')

        df = df_import[df_import['Remove'] != 1].reset_index(drop=True)

        # Rename columns
        df = df.rename(columns={'Gravidity (how many pregnancies have you had?)': 'Gravidity',
                                'Parity (number of live births)': 'Parity',
                                'random glucose': 'RandomGlucose',
                                'AGE': 'Age',
                                'Weight (kg)': 'Weight',
                                'Hb at delivery ': 'Hb Term',
                                'Mid upper arm circumstance ': 'MUAC',
                                'ID ': 'Id',
                                'EPDS score':'EPDS',
                                'Current BMI': 'BMI',
                                'GDM control': 'GDMControl',
                                'Maternal date of birth': 'MDOB',
                                'Problems during pregnancy': 'Problems',
                                'Mean Systolic': 'Systolic',
                                'Mean Diastolic ': 'Diastolic',
                                
                                })

        
        # Calculate Mean BP
        df['MAP'] = ((2 * df['Diastolic']) + df['Systolic'])/3


        # Clean Race
        df['Race'] = df['Race'].str.upper()
        df['Race'] = df['Race'].str.strip()
        df.loc[(df['Race'] == 'ASIAN'), 'Race'] = 'ASIAN EAST'
        df.loc[(df['Race'] == 'EAST ASIAN'), 'Race'] = 'ASIAN EAST'
        df.loc[(df['Race'] == 'SOUTH ASIAN'), 'Race'] = 'ASIAN SOUTH'
        df.loc[(df['Race'] == 'MIED'), 'Race'] = 'MIXED'

        # Clean 'Breastfeeding'
        df['Breastfeeding'] = df['Breastfeeding'].str.upper()
        df['Breastfeeding'] = df['Breastfeeding'].str.strip()

        df['BMI'] = df['BMI'].round(2)
        df['HbA1C'] = df['HbA1C'].astype(float)

        # Calculate eGFR
        df['b'] = 1
        df.loc[df['Race'] == 'BLACK', 'b'] = 1.159

        df['Creatinine (mg/dL)'] = df['Creatinine'] * 0.0113
        df['Creatinine (mg/dL)/k'] = df['Creatinine (mg/dL)'] / 0.7
        
        df['MIN'] = 1
        df.loc[df['Creatinine (mg/dL)/k'] < 1, 'MIN'] = df['Creatinine (mg/dL)/k']
        df['MIN'] = df['MIN'] ** -0.329

        df['MAX'] = 1
        df.loc[df['Creatinine (mg/dL)/k'] > 1, 'MAX'] = df['Creatinine (mg/dL)/k']
        df['MAX'] = df['MAX'] ** -1.209

        df['AGEADJ'] = 0.993 ** df['Age']

        df['eGFR'] = 141 * df['MIN'] * df['MAX'] * df['AGEADJ'] * 1.012 * df['b']

        # # Select subset of columns
        cols = ['Id', 'Age', 'Gravidity', 'Parity', 'BMI', 'Weight',
                'HbA1C', 'ACR', 'GDMControl', 'Race', 'eGFR', 'ALT',
                'MUAC', 'Hb', 'Hb Term', 'MDOB', 'Breastfeeding', 'EPDS', 'Systolic', 
                'Diastolic', 'MAP']
        df = df[cols]

        print(f"""Data consits of {len(df)} rows after cleaning. 
        * {len(df_import)-len(df)} rows have been excluded.
            """)

        return df
