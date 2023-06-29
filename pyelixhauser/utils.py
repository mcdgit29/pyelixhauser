'''
Internal utilities package that provides an streamlined load function
that loads the csv required from Elixhauser comorbity lookup
'''

import pkg_resources
import re
def load_resource(path):
    stream = pkg_resources.resource_string('pyelixhauser', path)
    results =str(stream).split('\\n')
    results = [item.strip() for _, item in enumerate(results) if len(item)>1]
    return results
