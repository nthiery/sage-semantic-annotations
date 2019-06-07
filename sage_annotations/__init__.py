"""
Semantic type annotations for the SageMath library

    sage: import sage_annotations
    sage: Semigroups().collect_semantic()
    {'elements': {'_mul_': {'__imfunc__': <abstract method _mul_ at ...>,
       'codomain': ParentOfSelf,
       'gap_name': '\\*',
       'mmt_name': '*'}},
     'gap': 'IsAssociative',
     'gap_negation': None,
     'gap_sub': None,
     'gap_super': None,
     'mmt': 'Semigroup',
     'morphisms': {},
     'parents': {'__truediv__': ...},
      '_an_element_': ...},
      'cardinality': {'__imfunc__': <abstract method cardinality at ...>,
       'codomain': *.sage(),
       'gap_name': 'Size',...},
      'is_d_trivial': ...,
      'is_finite': ...,
      'is_l_trivial': ...,
      'is_r_trivial': ...,
      'one': ...,
      'random_element': ...,
      'semigroup_generators': ...}}
"""

##############################################################################
# Monkey patch the Sage library upon importing this module
##############################################################################

import logging
from recursive_monkey_patch import monkey_patch

log_level=logging.ERROR

import sage_annotations.misc
import sage.misc
monkey_patch(sage_annotations.misc, sage.misc, log_level=log_level)

import sage_annotations.categories
import sage.categories
monkey_patch(sage_annotations.categories, sage.categories, log_level=log_level)

