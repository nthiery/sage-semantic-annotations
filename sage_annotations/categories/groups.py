from sage.misc.abstract_method import abstract_method
from sage.misc.sage_typing import semantic, Family, Sage, Self

@semantic(mmt="Group", variant="multiplicative")
class Groups:

    class ParentMethods:

        @semantic(gap="IsAbelian", codomain=Sage)
        @abstract_method
        def is_abelian(self):
            pass

        @semantic(gap="GeneratorsOfGroup", codomain=Family[Self])
        @abstract_method
        def group_generators(self):
            pass

        @semantic(gap=r"\/")
        @abstract_method
        def __truediv__(self, relators):
            pass
