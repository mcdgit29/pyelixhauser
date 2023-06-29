'''
Internal Test Methods to Unit Test  pyelixhauser package
'''

import logging
from pyelixhauser.setup_logger import logger

def test_cci():
    from pyelixhauser.cci import get_cci, _icd9_validation, _icd9_gen, cci_from_string, cci_from_array
    logger.debug('testing  cci module ....')
    assert get_cci("428.0") ==  'Diseases of the circulatory system'
    assert get_cci("") is None
    assert _icd9_validation("4280") == '4280'
    assert list(_icd9_gen("4280|4280")) == ['4280', '4280']
    assert list(_icd9_gen("")) == []
    assert cci_from_string('4280|4280,1611, 1, 0010').sum() == 2
    assert cci_from_array(['4280|4280', '1611, 1, 0010', '']).shape == (3, 18)
    assert cci_from_array(['4280|4280', '1611, 1, 0010', '']).sum().sum() == 2
    logger.info('testing  cci module complete')

def test_icd9cm():
    from pyelixhauser.icd9cm import _isin_range, _icd9_str_look_up, _icd9cm_lookup_df, _icd9_str_has_comorbity,comorbidity_from_string,comorbidity_from_array
    logger.debug('testing icd9cm module ... ')
    assert _isin_range('490.1', '490.x', '505.x')
    assert _isin_range('506.0', '490.x', '505.x') == False
    assert _icd9_str_look_up('490.1 | 506.0','490.x' )
    assert _icd9_str_has_comorbity("344.1" , "334.1, 342.x, 343.x, 344.0-\n344.6")
    assert _icd9_str_has_comorbity("344.7" , "334.1, 342.x, 343.x, 344.0-\n344.6") == False
    assert _icd9_str_has_comorbity("344.7" , "334.1, 342.x, 343.x, 344.0-\n344.6") == False
    assert(comorbidity_from_string("344.1").sum() == 1)
    assert comorbidity_from_string('440.1, 441.9').sum() == 1
    ref_str_array = _icd9cm_lookup_df.loc[:, "Enhanced ICD-9-CM"]

    assert comorbidity_from_string( ' , '.join(ref_str_array).replace('x', '1')).sum() == _icd9cm_lookup_df.shape[0]
    assert comorbidity_from_string('V45.1').sum() == 1
    assert comorbidity_from_string('').sum() ==0
    assert comorbidity_from_string('287.3').sum() ==1
    assert comorbidity_from_string('175').sum() ==1
    assert comorbidity_from_array([v.replace('x', '1') for v in ref_str_array ]).sum().sum() ==41
    assert comorbidity_from_array([v.replace('x', '1') for v in ref_str_array ]).shape[0] == ref_str_array.shape[0]
    logger.info('icd9cm module testing completed')

def test_icd10cm():
    from pyelixhauser.icd10cm import _parse_codes, _isin_range, comorbidity_from_string, comorbidity_from_array, _icd10cm_lookup_df, get_elix
    logger.debug('testing icd10cm module ....')
    assert _parse_codes('D51.1-D51.2') == ['D51.1', 'D51.2']

    assert _isin_range('D51.2','D51.x', 'D53.x')
    assert _isin_range('Z72.1', 'Z72.1')
    assert _isin_range('Z72.1', 'Z72.2') == False
    assert _isin_range('Z72.1', 'Z72.x')
    assert _isin_range('Z72.1', 'Z73.x') == False
    ref_str_array = _icd10cm_lookup_df.loc[:, "Enhanced ICD-9-CM"]

    assert comorbidity_from_string( ' , '.join(ref_str_array).replace('x', '1')).sum() == _icd10cm_lookup_df.shape[0]
    assert comorbidity_from_array([v.replace('x', '1') for v in ref_str_array ]).sum().sum() ==41
    assert comorbidity_from_array([v.replace('x', '1') for v in ref_str_array ]).shape[0] == ref_str_array.shape[0]
    assert get_elix('') is None
    assert get_elix('123') is None
    assert get_elix('abcd') is None
    assert get_elix('D67.1') == "Coagulopathy"
    assert get_elix('D68.1') == "Coagulopathy"
    assert get_elix('D69.1') == "Coagulopathy"
    assert get_elix('D69.5') == "Coagulopathy"
    assert get_elix('D69.7') is None
    assert get_elix('F22.23') == "Psychoses"
    logger.info('icd10cm module testing completed')

def test_icd10cm_cmr_2022():
    from pyelixhauser.icd10cm_cmr_v2022 import _icd10cm_validation, comorbidity_from_string, comorbidity_from_array, _idc10cm_lookup_df
    logger.debug('Testing icd10cm module ...')
    assert _idc10cm_lookup_df.shape[0] == 4319
    logger.debug(F'icd10cm map to ElixhauserComorbidity loaded with {_idc10cm_lookup_df.shape[0]} values')

    results = list(map(_icd10cm_validation, ["Z20.828", "J30.1", 'not an icd10cm']))
    assert comorbidity_from_string('E11.9 Z23, Z20.828 , J30.1, N18.3').sum() == 3
    logger.debug('comorbidity_from_string passed')

    results = comorbidity_from_array(['E11.9 Z23, Z20.828', 'J30.1', 'N18.3'])
    assert results.shape[0] == 3
    assert results.values.flatten().sum() == 4
    logger.info('Testing icd10cm module complete')


if __name__ == "__main__":
    logger.setLevel("DEBUG")
    logger.info('testing ElixhauserComorbidity package ...')
    test_cci()
    test_icd9cm()
    test_icd10cm()
    test_icd10cm_cmr_2022()
    logger.info('all tests completed for pyelixhauser package')
    print('test complete')
