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
    'eGFR': 'ml/minute/1.73m^2',
    'ACR': '',
    'RandomGlucose':'',
    'MUAC': 'cm',
    'Age': 'years',
    'Age Category': 'years',
    'BMI': '',
    'BMI Category': '',
    'EPDS':'score',
    'Percentage':'%',
    'Parity':'number of live births',
    'Race': 'race',
    'Systolic': '',
    'Diastolic': '',
}