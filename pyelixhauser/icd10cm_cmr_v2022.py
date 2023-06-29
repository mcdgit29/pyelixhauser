

'''
pyelixhauser icd10cm module contains
comorbidity_from_string,
comorbity_from_array methods for encoding icd10cm codes to Elixhauser Comorbidity


CMR-Reference-File-v2022




AIDS = AIDS/HIV
ALCOHOL = Alcohol Abuse
ANEMDEF = Anemia Defficiency
ARTH = Rheumatoid Arthritis
BLDLOSS = Blood Loss Anemia
CARDARRH = Cardiac Arrhythmia
CHF = Congestive Heart Failure
CHRNLUNG = Chronic Pulmonary Disease
COAG = Coagulopathy
DEPRESS = Depression
DM = Diabetes without Chronic Complications
DMCX = Diabetes with Chronic Complications
DRUG = Drug Abuse
HTN_C = Hypertension
HYPOTHY = Hypothyroidism
LIVER = Liver Disease
LYMPH = Lymphoma
LYTES = Fluid and Electrolyte Disorders
METS = Metastatic Cancer
NEURO = Other Neurological Disorders
OBESE = Obesity
PARA = Paralysis
PERIVASC = Peripheral Vascular Disease
PSYCH = Psychoses
PULMCIRC = Pulmonary Circulation Disorder
RENLFAIL = Renal Failure
TUMOR = Solid Tumor without Metastasis
ULCER = Peptic Ulcer Disease
VALVE = Valvular Disease
WGHTLOSS = Weight Loss
'''


import pkg_resources
import pandas as pd
import re
import logging
from pyelixhauser.setup_logger import logger
from pyelixhauser.utils import load_resource


_resource_name = "/resources/CMR-Reference-File-v2022-1.csv"
_manager = 'pyelixhauser'
_path = pkg_resources.resource_stream(_manager,_resource_name)

_idc10cm_lookup_df = pd.read_csv(_path, sep='\t', skiprows=1, index_col='ICD-10-CM Diagnosis')\
.sort_index()\
.drop('ICD-10-CM Code Description', axis=1)

_feature_names = list(_idc10cm_lookup_df.columns)
_null_result = pd.Series([0] * _idc10cm_lookup_df.shape[1], index=_feature_names)

def _icd10cm_validation(s):
    '''
    _icd10cm_validation
    internal function to return a valid icd10cm code from a string

    param s: string
    return string (contained valid icd10cm, or None if there is not one detected)
    '''


    s = ' ' + str(s).upper()
    s = re.sub('[^A-Z0-9.]', ' ', s).strip()
    s = re.sub('  ', ' ', s).strip()
    pattern = '^(?i:[A-TV-Z][0-9][0-9AB](?:\.[0-9A-KXZ](?:[0-9A-EXYZ](?:[0-9A-HX][0-59A-HJKMNP-S]?)?)?)?|U07(?:\.[01])?)$'
    try:
        results = re.search(pattern, s)
        return results.group()
    except AttributeError:
        logger.debug(F'failed to find an icd10cm in "{s}"')
        return None
    except TypeError:
        logger.debug(F'failed to find an icd10cm in "{s}"')
        return None

def _lookup_comorbility(code):
    '''
    internal function to lookup an icd10cm code  and comorbity
    param s: string (icd10cm code)
    return  pandas series, index is comorbities
    '''
    code = re.sub('[.]', '', code)
    try:
        result =  _idc10cm_lookup_df.loc[code, :]
        msg = F"{code}: resolved to comorbity {result.loc[result==1].index}"
        logger.debug(msg)
        return result
    except KeyError:
        logger.debug(F' Code {code} does not have an associated comorbidity')
        return _null_result


def _icd10cm_validated_code_gen(s, split=' '):
    '''
    internal generator that yields valid icd10cm codes
    param s: string (icd10cm code)
    param split: string, speratation character used to split multiple codes
    yields string (validated icd10cm code)


    '''
    list_of_tokens = re.split(split, s)

    for s in list(set(list_of_tokens)):
        result = _icd10cm_validation(s)
        if result:
            yield result


def _comorbidity_gen(s):
    '''
    internal generator that yields arrays of comorbities
    param s: string
    yield pandas series, index is comorbities
    '''
    s = ' ' + str(s).upper()
    s = re.sub('[^A-Z0-9.]', ' ', s).strip()
    s = re.sub('  ', ' ', s).strip()
    gen = _icd10cm_validated_code_gen(s)
    try:
        while True:
            code  = next(gen)
            yield _lookup_comorbility(code)
    except StopIteration:
        return _null_result

def comorbidity_from_string(s):
    '''
    comorbidity_from_string
    function to detect comorbities from a string if icd10cm codes
    param s: string (icd10cm codes shoulld be seperated with , or space )
    yield pandas series, index is comorbities

    example usage:
    comorbidity_from_string('E11.9 Z23, Z20.828 , J30.1, N18.3')


    '''

    results = pd.DataFrame(list(_comorbidity_gen(s)), columns=_feature_names)
    return results.max(axis=0)


def get_elix(s):
    '''
    get_elix(
    function to detect comorbities from a string if icd10cm codes
    param s: string (icd9cm codes shoulld be seperated with , or space )
    returns str

    example usage:
    get_elix('E11.9')


    '''
    array = comorbidity_from_string(s)
    array = array.iloc[1:]
    if array.sum() == 1:
        return array.loc[array == 1].index[0]
    elif array.sum() > 1:
        return  ' | '.join(array.loc[array == 1].index)
    else:
        return None
def comorbidity_from_array(array):
    '''
    comorbidity_from_string
    function to detect comorbities from a string if icd10cm codes
    param s: string (icd10cm codes shoulld be seperated with , or space )
    yield pandas series, index is comorbities

    example usage:
    comorbidity_from_string('E11.9 Z23, Z20.828 , J30.1, N18.3')


    '''

    results = list(map(comorbidity_from_string, array))
    return pd.DataFrame(results, columns=_feature_names)

