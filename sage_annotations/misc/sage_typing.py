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
import textwrap
import typing
from typing import Any, Iterator, List, Set

# We only import List, Set to be able to reimport from here
# This prevents pyflakes from complaining
typing.List, typing.Set

from sage.misc.abstract_method import AbstractMethod
from sage.misc.misc import attrcall
from sage.categories.category import Category
from sage.categories.category_with_axiom import CategoryWithAxiom
from sage.libs.gap.libgap import libgap
import sage.sets.family

class MMTWrap:
    def __init__(self,
                 mmt_name=None,
                 variant=None,
                 module=None):
        self.mmt_name = mmt_name
        self.variant = variant

def specialize(type, value):
    """
    Return a callable type that takes a GAP handle and make
    """
    if hasattr(type, "specialize"):
        return type.specialize(value)
    else:
        return type

def from_handle(type):
    if hasattr(type, "from_handle"):
        return type.from_handle
    else:
        return type

def GenericMeta_specialize(self, value):
    if self.__origin__ is None:
        return self
    return self.__origin__[specialize(self.__args__[0], value)]
typing.GenericMeta.specialize = GenericMeta_specialize


import mygap

def Any_from_handle(self, handle):
    return mygap.GAP(handle)
typing._Any.from_handle = Any_from_handle
def Iterator_from_handle(cls, handle):
    value_type = from_handle(cls.__args__[0])
    return itertools.imap(value_type, mygap.GAPIterator(handle))
Iterator.from_handle = classmethod(Iterator_from_handle)
def Container_from_handle(cls, handle):
    container_type = cls.__extra__
    if cls.__args__ is None:
        return container_type(handle)
    value_type = from_handle(cls.__args__[0])
    return container_type(value_type(x) for x in handle)
typing.Container.from_handle = classmethod(Container_from_handle)
class Family(typing.Sequence[typing.T]):
    __slots__ = ()
    __extra__ = sage.sets.family.TrivialFamily

Sage         = attrcall("sage")

# Class for dependent types constructed from a callable value -> type
# 
class DependentType(typing._TypingBase): # Singleton
    __metaclass__ = typing.TypingMeta
    __slots__ = ("name", "specialize")
    def __init__(self, specialize, name):
        self.name = name
        self.specialize = specialize
    def __instancecheck__(self, object):
        raise TypeError("Unspecialized {} cannot be used with isinstance()".format(self))
    def __repr__(self):
        return self.name

Self         = DependentType(lambda x: x,            name="Self")
FacadeFor    = DependentType(attrcall("facade_for"), name="FacadeFor")
ParentOfSelf = DependentType(attrcall("parent"    ), name="ParentOfSelf")


class Facade(typing.Sequence[typing.T]):

    @classmethod
    def from_handle(cls, handle):
        value_type = cls.__args__[0]
        result = mygap.GAP(handle)
        result._refine_category_(result.category().Facade())
        result.facade_for = lambda: value_type
        return result



def gap_handle(x):
    """
    Return a low-level libgap handle to the corresponding GAP object.

    EXAMPLES::

        sage: from mygap import mygap
        sage: from mmt import gap_handle
        sage: h = libgap.GF(3)
        sage: F = mygap(h)
        sage: gap_handle(F) is h
        True
        sage: l = gap_handle([1,2,F])
        sage: l
        [ 1, 2, GF(3) ]
        sage: l[0] == 1
        True
        sage: l[2] == h
        True

    .. TODO::

        Maybe we just want, for x a glorified hand, libgap(x) to
        return the corresponding low level handle
    """
    from mygap import GAPObject
    if isinstance(x, (list, tuple)):
        return libgap([gap_handle(y) for y in x])
    elif isinstance(x, GAPObject):
        return x.gap()
    else:
        return libgap(x)

def mmt_lookup_signature(*args):
    raise NotImplementedError

class MMTWrapMethod(MMTWrap):
    """

    .. TODO:: add real tests

    EXAMPLES::

        sage: from mmt import MMTWrapMethod
        sage: def zero(self):
        ....:     pass
        sage: f = MMTWrapMethod(zero, "0", gap_name="Zero")
        sage: c = f.generate_code("NeutralElement")
        sage: c
        <function zero at ...>
    """
    def __init__(self, f, mmt_name=None, gap_name=None, codomain=None, **options):
        MMTWrap.__init__(self, mmt_name, **options)
        self.__imfunc__= f
        self.gap_name = gap_name
        self.codomain = codomain
        if isinstance(f, AbstractMethod):
            f = f._f
        argspec = sage.misc.sageinspect.sage_getargspec(f)
        self.arity = len(argspec.args)

    def generate_code(self, mmt_theory):
        codomain = self.codomain
        arity = self.arity
        gap_name = self.gap_name
        if gap_name is None: # codomain is None
            signature = mmt_lookup_signature(mmt_theory, self.mmt_name)
            if signature is not None:
                domains, codomain = signature
                arity = len(domains)
                if self.arity is not None:
                    assert self.arity == arity
                # TODO: cleanup this logic
                if all(domain == codomain for domain in domains):
                    codomain = ParentOfSelf
                    assert self.codomain is None or codomain == self.codomain
        assert arity is not None
        assert gap_name is not None
        if codomain is None:
            codomain = Any
        #assert isinstance(codomain, DependentType)
        def wrapper_method(self, *args):
            return from_handle(specialize(codomain, self))(getattr(libgap, gap_name)(*gap_handle((self,)+args)))
        wrapper_method.__name__ = self.__imfunc__.__name__
        wrapper_method.__doc__ = textwrap.dedent("""
        Wrapper around GAP's method {}

        arity: {}
        codomain: {}
        """).format(gap_name, arity, codomain)
        return wrapper_method

nested_classes_of_categories = [
    "ParentMethods",
    "ElementMethods",
    "MorphismMethods",
    "SubcategoryMethods",
]

def generate_interface(cls, mmt=None, gap=None, gap_super=None, gap_sub=None, gap_negation=None):
    """
    INPUT:
    - ``cls`` -- the class of a category
    - ``mmt`` -- a string naming an mmt theory
    - ``gap`` -- a string naming a gap property/category
    """
    # Fetch cls.GAP, creating it if needed
    try:
        # Can't use cls.GAP because of the binding behavior
        GAP_cls = cls.__dict__['GAP']
    except KeyError:
        GAP_cls = type(cls.__name__+".GAP", (CategoryWithAxiom,), {})
        GAP_cls.__module__ = cls.__module__
        setattr(cls, 'GAP', GAP_cls)

    # Store the semantic information for later use
    cls._semantic={
        'gap': gap,
        'gap_sub': gap_sub,
        'gap_super': gap_super,
        'gap_negation': gap_negation,
        'mmt': mmt,
    }

    # Fill the database mapping gap categories / properties to their
    # corresponding (super) Sage categories
    if gap_sub is None:
        gap_sub = gap
    if gap_sub is not None or gap_negation is not None:
        def fill_allignment_database(cls, source=None):
            assert issubclass(cls, Category)
            import mygap
            if gap_sub is not None:
                mygap.gap_category_to_structure[gap_sub] = mygap.add(category=cls)
            if gap_negation is not None:
                mygap.false_properties_to_structure[gap_negation] = mygap.add(category=cls)
        if issubclass(cls, Category):
            fill_allignment_database(cls)
        else:
            # cls is a fake class whose content will be monkey patched to an actual category
            # Delay the database filling until the monkey patching, so
            # that will actually know the category class
            cls._monkey_patch_hook = classmethod(fill_allignment_database)

    # Recurse in nested classes
    for name in nested_classes_of_categories:
        try:
            source = getattr(cls, name)
        except AttributeError:
            continue
        # Fetch the corresponding class in cls.GAP, creating it if needed
        try:
            target = getattr(GAP_cls, name)
        except AttributeError:
            target = type(name, (), {})
            setattr(GAP_cls, name, target)
        nested_class_semantic = {}
        for (key, method) in source.__dict__.items():
            if key in {'__module__', '__doc__'}:
                continue
            assert isinstance(method, MMTWrapMethod)
            nested_class_semantic[key] = {
                "__imfunc__": method.__imfunc__,
                "codomain" : method.codomain,
                "gap_name" : method.gap_name,
                "mmt_name" : method.mmt_name
            }
            setattr(target, key, method.generate_code(mmt))
            setattr(source, key, method.__imfunc__)
        source._semantic = nested_class_semantic

def semantic(mmt=None, variant=None, codomain=None, gap=None, gap_negation=None, gap_sub=None, gap_super=None):
    def f(cls_or_function):
        if inspect.isclass(cls_or_function):
            cls = cls_or_function
            generate_interface(cls, mmt=mmt, gap=gap, gap_negation=gap_negation, gap_sub=gap_sub, gap_super=gap_super)
            return cls
        else:
            return MMTWrapMethod(cls_or_function,
                                 mmt_name=mmt,
                                 variant=variant,
                                 codomain=codomain,
                                 gap_name=gap)
    return f
