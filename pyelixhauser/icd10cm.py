

'''
pyelixhauser icd9cm module contains
comorbidity_from_string,
comorbity_from_array methods for encoding icd9cm codes to Elixhauser Comorbidity
sourced from



http://mchp-appserv.cpe.umanitoba.ca/concept/Elixhauser%20Comorbidities%20-%20Coding%20Algorithms%20for%20ICD-9-CM%20and%20ICD-10.pdf

this table was recreated as a csv to store data for the icd9cm Elixhauser map

Quan H, Sundararajan V, Halfon P, et al. Coding algorithms for defining Comorbidities in ICD-9-CM and
ICD-10 administrative data. Med Care. 2005 Nov; 43(11): 1130-9
example inputs

['Congestive heart failure ', 'Cardiac arrhythmias ', 'Valvular disease',
       'Pulmonary circulation Disorders', 'Peripheral vascular disorders',
       'Hypertension, uncomplicated', 'Hypertension, complicated', 'Paralysis',
       'Other neurological disorders ', 'Chronic pulmonary disease ',
       'Diabetes, uncomplicated ', 'Diabetes, complicated', 'Hypothyroidism ',
       'Renal failure', 'Liver disease',
       'Peptic ulcer disease excluding bleeding', 'AIDS/H1V ', 'Lymphoma ',
       'Metastatic cancer ', 'Solid tumor without Metastasis',
       'Rheumatoid arthritis/ collagen vascular diseases', 'Coagulopathy ',
       'Obesity ', 'Weight loss', 'Fluid and electrolyte Disorders',
       'Blood loss anemia', 'Deficiency anemia', 'Alcohol abuse ',
       'Drug abuse', 'Psychoses', 'Depression']



'''


import pkg_resources
import pandas as pd
import re
import logging
from pyelixhauser.setup_logger import logger
from pyelixhauser.utils import load_resource


_resource_name = "/resources/icd10_elixhauser.csv"
_manager = 'pyelixhauser'
_path = pkg_resources.resource_stream(_manager,_resource_name)

_icd10cm_lookup_df = pd.read_csv(_path)
_feature_names = _icd10cm_lookup_df.loc[:, 'Comorbidities']
_feature_names = [n.replace('\n', ' ' ).strip() for n in _feature_names]

def _parse_codes(s, pattern='[A-Z][0-9]+[.]?x?[0-9]*'
):
    return re.findall(pattern, s)



def _isin_range(s, min_code, max_code= None):
    s = str(s).lower().replace('\n', '').replace('\t', '').strip()
    min_code = str(min_code).lower().replace('\n', '').replace('\t', '').strip()
    if max_code is None:
        max_code = min_code
    else:
        max_code =str(max_code).lower().replace('\n', '').replace('\t', '').strip()
    logger.debug(F'checking inputs {s} is in range {min_code, max_code} ..')
    if all((s[0]==min_code[0], s[0]==max_code[0])):
        s = s[1:]
        min_code = min_code[1:]
        max_code = max_code[1:]
        try:
            v = float(s)
        except ValueError:
            logger.debug(F'input string  {s} to _isin_range in not in range {min_code, max_code}')
            return False

        if all(('x' in min_code, 'x' in max_code)):
            try:
                min_val = float(re.sub('x', '', min_code))
                max_val = float(re.sub('x', '', max_code)) + 1
                if all((v>=min_val, v< max_val)):
                    return True
                else:
                    return False
            except ValueError:
                logger.debug(F'input string  {s} to _isin_range in not in range {min_code, max_code}')
                return False

        if any(('x' in min_code, 'x' in max_code)):
            try:
                min_val = float(re.sub('x', '', min_code))
                max_val = float(re.sub('x', '', max_code)) + 1
                if all((v>=min_val, v< max_val)):
                    return True
                else:
                    return False
            except ValueError:
                logger.debug(F'input string  {s} to _isin_range in not in range {min_code, max_code}')
                return False
        else:
            try:
                min_val = float(min_code)
                max_val = float(max_code)
                if all((v>=float(min_val), v<= float(max_val))):
                    return True
                else:
                    return False
            except ValueError:
                return False
    else:
        return False

def _icd_str_look_up(input_str, ref_str):
    input_codes = _parse_codes(input_str)
    reference_codes = _parse_codes(ref_str)
    ## Single reference code
    if len(reference_codes ) == 1:
        if 'x' in reference_codes[0]:
            isin_results = [_isin_range(code,reference_codes[0],reference_codes[0]) for code in input_codes]
        else:
            isin_results = [code == reference_codes[0] for code in input_codes]
        return any(isin_results)

    elif len(reference_codes ) == 2:
        isin_results = [_isin_range(code,reference_codes[0],reference_codes[1]) for code in input_codes]
        return any(isin_results)
    elif len(reference_codes) == 0:
        return False
    else:
        raise ValueError(F" multipe reference code {reference_codes } ranges with 3 or more codes not supported")

def _icd_str_has_comorbity(input_str, ref_str):
    ref_str = ref_str.replace('\n', '')
    ref_code_ranges =[c.strip() for c in  ref_str.split(',')]
    results = list(map(lambda x: _icd_str_look_up(input_str, x),     ref_code_ranges))
    return any(results)



def comorbidity_from_string(s):
    '''
    comorbidity_from_string
    function to detect comorbities from a string if icd10cm codes
    param s: string (icd10cm codes shoulld be seperated with , or space )
    returns pandas series, index is comorbities

    example usage:
    comorbidity_from_string('K29.2 | K70.0')


    '''
    ref_str_array = _icd10cm_lookup_df.loc[:, "Enhanced ICD-9-CM"]
    results = list(map(lambda x: _icd_str_has_comorbity(s, x), ref_str_array))
    return pd.Series(results, index=_feature_names).replace({True:1, False:0})

def get_elix(s):
    '''
    get_elix(
    function to detect comorbities from a string if icd10cm codes
    param s: string (icd10cm codes shoulld be seperated with , or space )
    returns str

    example usage:
    get_elix('Z71.5')


    '''
    array = comorbidity_from_string(s)
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
    yield pandas series, index is comorbities from ICD9 cm codes

    example usage:
    comorbidity_from_string(' F34.1','K29.2 | K70.0')


    '''

    results = list(map(comorbidity_from_string, array))
    return pd.DataFrame(results, columns=_feature_names)

