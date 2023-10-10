import os
import sys


ROOTDIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#print(ROOTDIR)

UPDATEALL = False

UOM = {
    'HbA1C': 'mmol/mol',
    'HbA1C Category': 'mmol/mol',
    'Hb': 'mg/dL',
    'Hb Category': 'mg/dL',
    'ALT': 'U/L',
    'Creatinine': 'mg/dL',
    'eGFR': 'ml/minute/1.73m<sup>2</sup>',
    'ACR': '',
    'RandomGlucose':'',
    'MUAC': 'cm',
    'Age': 'years',
    'Age Category': 'years',
    'BMI': 'kg/m<sup>2</sup>',
    'BMI Category': 'kg/m<sup>2</sup>',
    'EPDS':'score',
    'Percentage':'%',
    'Parity':'number of live births',
    'Race': 'race',
    'Systolic': 'mmHg',
    'Diastolic': 'mmHg',
    'MAP': 'mmHg',
    'Count': 'number of patients',
    'Bars': '',
}

FIGFOLDER = os.path.join(ROOTDIR, "images", "202310")