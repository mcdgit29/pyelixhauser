# pyelixhauser A package to encode Comorbidity

## Introduction
Pyelixhauser is a python package intended extract comorbidity information from  
International Classification of Disease code (ICD) codes.  
This package supports both ICD10-CM, ICD9-CM in different modules.  
It has the capability of detecting when a comorbidity is present in a string or list of strings for ICD codes.  
This package uses the Elixhauser and Charlson comorbidity indecies that were developed to stratify patient's mortality
risk (1).

The package contains four modules when methods available for use.
 
	+ cci : Charleson Comorbity (ICD9CM) (3)
	+ icd9cm: Elixhauser Comorbidity  on ICD9CM (4)
	+ icd10cm: Elixhauser Comorbidity  on ICD10CM (4)
	+ icd10cm_cmr_v_2022: Elixhauser Comorbidity  on ICD10CM adapted from the  Agency for Healthcare Research and Quality 2022 SAS Software (2)


## Methods
This package implements three basic methods for each module
      + get_elix: returns a  comorbidity string from a single ICD code
      + comorbidity_from_string, returns a binary encoded array of comorbidity for a string containing multiple codes
      + comorbidity_from_array, returns a data from of binary encoded comorbidity, one row for each str  in a list of strings 




Example of using CCI functions
```python
from pyelixhauser.cci import cci_from_string, cci_from_array
results = cci_from_string('V45.1')
print(results)
```

Example of using elixhauser functions
```python
from pyelixhauser.icd9cm import get_elix
results = get_elix("344.1")
print(results)
```

Example of using ICD10cm Elixhauser functions 
For usage when input is a string (with multiple icd10cm codes sperated by a space, comma)
```python
from pyelixhauser.icd10cm import comorbidity_from_string, comorbidity_from_array

## returns a pandas series
results =  comorbidity_from_string('E11.9 Z23, Z20.828 , J30.1, N18.3')
print(results)
```


For usage when the input is a array of strings (each of which can contain multiple ICD10cm codes)
```python
## returns a pandas data frame
results = comorbidity_from_array(['E11.9 Z23, Z20.828', 'J30.1', 'N18.3'])
print(results)
```

#### Example Outputs


		# Comorbidities 	AIDS 	ALCOHOL 	ANEMDEF 	AUTOIMMUNE 	BLDLOSS 	CANCER_LEUK 	CANCER_LYMPH 	CANCER_METS 	CANCER_NSITU 	... 	PERIVASC 	PSYCHOSES 	PULMCIRC 	RENLFL_MOD 	RENLFL_SEV 	THYROID_HYPO 	THYROID_OTH 	ULCER_PEPTIC 	VALVE 	WGHTLOSS
		0 	1 	0 	0 	0 	0 	0 	0 	0 	0 	0 	... 	0 	0 	0 	0 	0 	0 	0 	0 	0 	0
		1 	0 	0 	0 	0 	0 	0 	0 	0 	0 	0 	... 	0 	0 	0 	0 	0 	0 	0 	0 	0 	0
		2 	1 	0 	0 	0 	0 	0 	0 	0 	0 	0 	... 	0 	0 	0 	1 	0 	0 	0 	0 	0 	


Current column headers in the reference file are:


	# Comorbidities	AIDS	ALCOHOL	ANEMDEF	AUTOIMMUNE	BLDLOSS	CANCER_LEUK	CANCER_LYMPH	CANCER_METS	CANCER_NSITU	CANCER_SOLID	CBVD_POA	CBVD_SQLA	COAG	DEMENTIA	DEPRESS	DIAB_CX	DIAB_UNCX	DRUG_ABUSE	HF	HTN_CX	HTN_UNCXLIVER_MLD	LIVER_SEV	LUNG_CHRONIC	NEURO_MOVT	NEURO_OTH	NEURO_SEIZ	OBESE	PARALYSIS	PERIVASC	PSYCHOSES	PULMCIRCRENLFL_MOD	RENLFL_SEV	THYROID_HYPO	THYROID_OTH	ULCER_PEPTIC	VALVE	WGHTLOS


```python

from pyelixhauser.icd9cm import comorbidity_from_string, comorbidity_from_array

## returns a pandas series
results =  comorbidity_from_string('V45.1')
print(results)
```


## License
This package is considered as-is software, and the maintainers make no commitments it’s usability, maintenance, accuracy or security. This software is licensed with Mozilla Public Licence 2.0


## References
1. Sharma N, Schwendimann R, Endrich O, Ausserhofer D, Simon M. Comparing Charlson and Elixhauser comorbidity indices with different weightings to predict in-hospital mortality: an analysis of national inpatient data. BMC Health Services Research. 2021;21(1):13. doi:10.1186/s12913-020-05999-5
2. Elixhauser Comorbidity Software Refined for ICD-10-CM. Accessed June 29, 2023. https://hcup-us.ahrq.gov/toolssoftware/comorbidityicd10/comorbidity_icd10.jsp
3. Charlson ME, Pompei P, Ales KL, MacKenzie CR. A new method of classifying prognostic comorbidity in longitudinal studies: development and validation. J Chronic Dis. 1987;40(5):373-383. doi:10.1016/0021-9681(87)90171-8
4. Elixhauser A, Steiner C, Harris DR, Coffey RM. Comorbidity measures for use with administrative data. Med Care. 1998;36(1):8-27. doi:10.1097/00005650-199801000-00004


## Supplemental Materials 

### CCI Support
sourced from
Chronic Condictions idicators from ICD9cm  codes
https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp

### ICD9cm Elixhauser Support
currently supports one hot encoded conditions (but not overall index calculation )

http://mchp-appserv.cpe.umanitoba.ca/concept/Elixhauser%20Comorbidities%20-%20Coding%20Algorithms%20for%20ICD-9-CM%20and%20ICD-10.pdf

this table was recreated as a csv to store data for the icd9cm Elixhauser map


####  Defintions of Elixhauser / User Guide

This python package uses the source data from the CMR SAS package, and the formal defintions all variables reside here:

https://www.hcup-us.ahrq.gov/toolssoftware/comorbidityicd10/CMR-User-Guide-v2022-1.pdf

#### Source Data
This tool is uses CMR Reference v2022-1
found here  

https://www.hcup-us.ahrq.gov/toolssoftware/comorbidityicd10/CMR-Reference-File-v2022-1.xlsx

#### To update this code for a new CMR version
if a new version of  Elixhauser Comorbidity Indices is to be integrated, the new Reference
file from needs to be added as a csv to /resources, and the path in
icd10cm.py
_resource_name = "/resources/CMR-Reference-File-v2022-1.csv" needs to be updated to the
new file.
