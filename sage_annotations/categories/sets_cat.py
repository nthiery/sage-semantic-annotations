from sage.misc.abstract_method import abstract_method
from sage.misc.sage_typing import semantic, FacadeFor, List, Sage, Self
from sage.categories.category_with_axiom import CategoryWithAxiom

@semantic(mmt="Set")
class Sets:
    class ParentMethods:
        @semantic(gap="IsFinite", codomain=Sage)
        @abstract_method
        def is_finite(self):
            pass

        @semantic(gap="Size", codomain=Sage)
        @abstract_method
        def cardinality(self):
            pass

        @semantic(gap="Representative", codomain=Self)
        @abstract_method
        def _an_element_(self):
            pass

        @semantic(gap="Random", codomain=Self)
        @abstract_method
        def random_element(self):
            pass

    @semantic(mmt="TODO", gap="IsFinite")
    class Finite:
        class ParentMethods:
            @semantic(gap="List", codomain=List[Self])
            @abstract_method
            def list(self):
                pass

        @semantic()
        class Facade(CategoryWithAxiom):
            class ParentMethods:
                @semantic(gap="List", codomain=List[FacadeFor])
                @abstract_method
                def list(self):
                    pass

    @semantic(gap_negation="IsFinite")
    class Infinite:
        pass
