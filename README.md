# sage-semantic-annotations: Semantic annotations for SageMath

This [SageMath](http://sagemath.org) package adds (some) annotations
to the SageMath library that provides semantic information such as:

- signature of methods

- alignments to other systems: what is the name of this category or
  this method in this other system? Currently, alignments are mostly
  with the MMT system (for formalization) and the
  [GAP](http://gap-system.org/) system.

- mathematical relevance: some indication of how important a given
  method is for some algebraic structure: part of the definition of
  the structure? An important invariant? A computationally cheap or
  expensive.

In practice, the annotations take the form of a decorator `@semantic`
to the relevant classes or (abstract) methods. Here is an example:

    @semantic(mmt="Set")
    class Sets:
        class ParentMethods:
            ...

            @semantic(gap="Size", codomain=Union[NN, Infinity])
            @abstract_method
            def cardinality(self):
                pass

The above states that the Sage category `Sets` (which provides code,
tests, and documentation for sets, their elements and morphisms),
implements the notion formalized as "Set" in MMT. In addition, the
cardinality method, formalized as `#` in MMT, returns an integer or
infinity, and is called `Size` in GAP.


Eventually, these alignments would naturally go in the Sage library
itself. To ease the transition, this package is laid out following the
Sage library module and class structure. For example, the above
snippet, taken from in
[`sage_annotations.categories.sets_cat`](sage_annotations/categories/sets_cat.py)
contains just the items that need to be inserted in the existing Sage
class `Sets` from the module `sage.categories.sets_cat`.

The insertion is done upon loading the package, using
[recursive_monkey_patch](https://github.com/nthiery/recursive-monkey-patch).
