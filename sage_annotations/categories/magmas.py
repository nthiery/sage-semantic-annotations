from sage.misc.abstract_method import abstract_method
from sage.misc.sage_typing import semantic, ParentOfSelf, Self
import sage.categories.magmas

@semantic(mmt="Magma", gap="IsMagma", variant="multiplicative")
class Magmas:
    class ElementMethods:
        @semantic(mmt="*", gap=r"\*", codomain=ParentOfSelf) #, operator="*"
        @abstract_method
        def _mul_(self, other):
            pass

    class ParentMethods:
        one = semantic(mmt="neutral", gap="One", codomain=Self)(sage.categories.magmas.Magmas.Unital.ParentMethods.__dict__['one'])

    @semantic(mmt="NeutralElement", gap="IsMagmaWithOne")
    class Unital:
        class ParentMethods:
            # Defined in NeutralElementLeft
            # - How to retrieve it?
            # - How to detect that this is a method into self?
            #one = semantic(mmt="neutral", gap="One", codomain=Self)(sage.categories.magmas.Magmas.Unital.ParentMethods.__dict__['one'])
            #@abstract_method
            #def one(self):
            #    # Generates automatically in the XXX.GAP category
            #    # def one(self): return self(self.gap().One())
            #    pass
            pass

        class ElementMethods:
            @semantic(mmt="inverse", gap="Inverse", codomain=ParentOfSelf)
            @abstract_method
            def __invert__(self): # TODO: deal with "fail"
                pass

        @semantic(gap="IsMagmaWithInverses")
        class Inverse:
            pass

    @semantic(gap="IsCommutative")
    class Commutative:
        pass
