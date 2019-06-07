from sage.misc.sage_typing import semantic, FacadeFor, Iterator, Self
from sage.misc.abstract_method import abstract_method
from sage.categories.category_with_axiom import CategoryWithAxiom

@semantic(mmt="TODO") # TODO gap=""????
class EnumeratedSets:
    class ParentMethods:
        @semantic(gap="Iterator", codomain=Iterator[Self])
        @abstract_method
        def __iter__(self):
            pass
    @semantic(gap_sub="IsList")
    class Finite:
        pass

    @semantic()
    class Facade(CategoryWithAxiom):
        class ParentMethods:
            @semantic(gap="Iterator", codomain=Iterator[FacadeFor])
            @abstract_method
            def __iter__(self):
                pass
