
import pkg_resources
import pandas as pd
import re
import logging
from pyelixhauser.setup_logger import logger
from pyelixhauser.utils import load_resource
import numpy as np

'''


https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp
1 = Infectious and parasitic disease

2 = Neoplasms

3 = Endocrine, nutritional, and metabolic diseases and immunity disorders

4 = Diseases of blood and blood-forming organs

5 = Mental disorders

6 = Diseases of the nervous system and sense organs

7 = Diseases of the circulatory system

8 = Diseases of the respiratory system

9 = Diseases of the digestive system

10 = Diseases of the genitourinary system

11 = Complications of pregnancy, childbirth, and the puerperium

12 = Diseases of the skin and subcutaneous tissue

13 = Diseases of the musculoskeletal system

14 = Congenital anomalies

15 = Certain conditions originating in the perinatal period

16 = Symptoms, signs, and ill-defined conditions

17 = Injury and poisoning

18 = Factors influencing health status and contact with health services

'''


_resource_name = "/resources/cci2015.csv"
_manager = 'pyelixhauser'
_path = pkg_resources.resource_stream(_manager,_resource_name)


_input_cols = ['ICD-9-CM CODE',
	       'ICD-9-CM CODE DESCRIPTION',
    	   'CATEGORY DESCRIPTION',
           'BODY SYSTEM']
_cci_dict = {
1 : 'Infectious and parasitic disease',

2 : 'Neoplasms',

3 : 'Endocrine, nutritional, and metabolic diseases and immunity disorders',

4 : 'Diseases of blood and blood-forming organs',

5 : 'Mental disorders',

6 : 'Diseases of the nervous system and sense organs',

7 : 'Diseases of the circulatory system',

8 : 'Diseases of the respiratory system',

9 : 'Diseases of the digestive system',

10 : 'Diseases of the genitourinary system',

11 : 'Complications of pregnancy, childbirth, and the puerperium',

12 : 'Diseases of the skin and subcutaneous tissue',

13 : 'Diseases of the musculoskeletal system',

14 : 'Congenital anomalies',

15 : 'Certain conditions originating in the perinatal period',

16 : 'Symptoms, signs, and ill-defined conditions',

17 : 'Injury and poisoning',

18 : 'Factors influencing health status and contact with health services'
}
_cci_df = pd.read_csv(_path, skiprows=2, index_col=None, names=_input_cols)
_cci_df.loc[:, 'ICD-9-CM CODE'] = _cci_df.loc[:, 'ICD-9-CM CODE']\
.apply(lambda x: re.sub('[^0-9A-Z]','', str(x).upper()).strip())

def _is_substring(s_input, s_ref):
	s_input = str(s_input).replace('.', '').upper().strip()
	if len(str(s_input)) == 0:
		return False
	if s_ref.startswith(s_input):
		return True
	else:
		return False


def _get_cci(s):
	index = _cci_df.loc[:, 'ICD-9-CM CODE'].apply(lambda x: _is_substring(s, x))
	results = _cci_df.loc[index, ['CATEGORY DESCRIPTION','BODY SYSTEM']]
	try:
		category = int(re.sub('[^0-9]','',(results.iloc[0,1])))
		is_chronic = int(re.sub('[^0-9]','',results.iloc[0,0])) == 1
		logger.debug(F'cci lookup hit found in {s}')
		return category, is_chronic
	except IndexError:
		return (None, False)


def _icd9_validation(s):
	pattern ="V?[0-9]{2,8}"

	s = ' ' + str(s).upper()
	s = re.sub('[.]', '', s).strip()
	logger.debug(F"icd9 validation function for {s}")
	try:
	    results = re.search(pattern, s)
	    return results.group()
	except AttributeError:
	    logger.debug(F'failed to find an icd9 in "{s}"')
	    return None
	except TypeError:
	    logger.debug(F'failed to find an icd9 in "{s}"')
	    return None


def _icd9_gen(s):
		s = re.sub('[^V0-9.]', ' ', s).strip()
		s = re.sub('  ', ' ', s).strip()
		for result in re.findall("V?[0-9]{2,8}", s):
			yield _icd9_validation(result)


def cci_from_string(s):
	icd9_list = list(_icd9_gen(s))
	cci_tuples = list(map(_get_cci, icd9_list))
	index = list(_cci_dict.values())
	results = pd.Series(np.zeros(len(index)), index = index).astype(int)
	for (i, b) in cci_tuples:
		if b:
			results.loc[_cci_dict[i]] = 1
		else:
			pass
	return results
def cci_from_array(array):
	index = list(_cci_dict.values())
	results = np.zeros((len(array), len(index )))
	for (i, s) in enumerate(array):
		results[i, :] = cci_from_string(s)
	return pd.DataFrame(results, columns=index).astype(int)


def get_cci(s):
    '''
    get_cci(
    function to detect comorbities from a string if icd9 codes
    param s: string (icd9cm codes shoulld be seperated with , or space )
    returns str

    example usage:
    get_elix(('490.1')


    '''
    array = cci_from_string(s)
    if array.sum() == 1:
        return array.loc[array == 1].index[0]
    elif array.sum() > 1:
        return  ' | '.join(array.loc[array == 1].index)
    else:
        return None
