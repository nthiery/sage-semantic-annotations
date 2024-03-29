"""
Sage extensions to Python's typing library

EXAMPLES::

    sage: import sage_annotations
    sage: from sage.misc.sage_typing import semantic, FacadeFor, List, Sage, Self

    sage: from sage.misc.sage_typing import Family, Iterator, List, Set, ParentOfSelf, Self, Sage
    sage: Self
    Self
    sage: ParentOfSelf
    ParentOfSelf
    sage: from typing import Iterator, Set, List
    sage: Family[Iterator[Set[List[Self]]]]
    sage.misc.sage_typing.Family[typing.Iterator[typing.Set[typing.List[Self]]]]
"""
import itertools

import inspect
import typing
from typing import Any, Iterator, List, Tuple, Set, _GenericAlias

# We only import List, Set to be able to reimport from here
# This prevents pyflakes from complaining
Any, List, Set, Iterator

from sage.misc.abstract_method import AbstractMethod
from sage.misc.call import attrcall
from sage.categories.category import Category
from sage.libs.gap.libgap import libgap
import sage.sets.family

def specialize(type, value):
    """
    Return a callable type that takes a GAP handle and make
    """
    if hasattr(type, "specialize"):
        return type.specialize(value)
    else:
        return type

def GenericMeta_specialize(self, value):
    return self.copy_with(tuple(specialize(a, value) for a in self.__args__))
_GenericAlias.specialize = GenericMeta_specialize

Family = _GenericAlias(sage.sets.family.TrivialFamily, typing.T)
class _Facade:
    pass
Facade = _GenericAlias(_Facade, typing.T)

Sage         = attrcall("sage")

# Class for dependent types constructed from a callable value -> type
# 
class DependentType:#(typing._TypingBase): # Singleton
    #__metaclass__ = typing.TypingMeta
    __slots__ = ("name", "specialize")
    # Should be callable?
    def __init__(self, specialize, name):
        self.name = name
        self.specialize = specialize
    def __instancecheck__(self, object):
        raise TypeError("Unspecialized {} cannot be used with isinstance()".format(self))
    def __repr__(self):
        return self.name
    def __call__(self, o):
        pass

Self         = DependentType(lambda x: x,            name="Self")
FacadeFor    = DependentType(attrcall("facade_for"), name="FacadeFor")
ParentOfSelf = DependentType(attrcall("parent"    ), name="ParentOfSelf")

class WrapMethod:
    """

    .. TODO:: add real tests

    EXAMPLES::

        sage: from sage.misc.sage_typing import WrapMethod
        sage: def zero(self):
        ....:     pass
        sage: f = WrapMethod(zero, gap_name="Zero")
        sage: f.semantic
        {'argspec': ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None),
        'arity': 1,
        'gap_name': 'Zero'}
        sage: c = f.generate_code("NeutralElement") # not tested
        sage: c                                     # not tested
        <function zero at ...>
    """
    def __init__(self, f, **options):
        self.__imfunc__= f
        self.semantic = dict(options)
        if isinstance(f, AbstractMethod):
            f = f._f
        argspec = sage.misc.sageinspect.sage_getargspec(f)
        self.semantic['argspec']= argspec
        self.semantic['arity'] = len(argspec.args)


nested_classes_of_categories = [
    "ParentMethods",
    "ElementMethods",
    "MorphismMethods",
    "SubcategoryMethods",
]

annotated_categories = []

def register_annotated_category(cls, source=None):
    assert issubclass(cls, Category)
    annotated_categories.append(cls)

def harvest_class(cls, **options):
    """
    INPUT:
    - ``cls`` -- the class of a category
    - ``mmt`` -- a string naming an mmt theory
    - ``gap`` -- a string naming a gap property/category
    """

    # Store the semantic information for later use
    cls._semantic=dict(options)

    if issubclass(cls, Category):
        register_annotated_category(cls)
    else:
        # cls is a fake class whose content will be monkey patched to an actual category
        # Delay the database filling until the monkey patching, so
        # that will actually know the category class
        cls._monkey_patch_hook = classmethod(register_annotated_category)

    # Recurse in nested classes
    for name in nested_classes_of_categories:
        try:
            source = getattr(cls, name)
        except AttributeError:
            continue
        nested_class_semantic = {}
        for (key, method) in source.__dict__.items():
            if key in {'__module__', '__doc__','__dict__', '__weakref__'}:
                continue
            if isinstance(method, WrapMethod):
                nested_class_semantic[key] = method.semantic
                setattr(source, key, method.__imfunc__)
        source._semantic = nested_class_semantic

def semantic(**options):
    def f(cls_or_function):
        if inspect.isclass(cls_or_function):
            cls = cls_or_function
            harvest_class(cls, **options)
            return cls
        else:
            return WrapMethod(cls_or_function, **options)
    return f
