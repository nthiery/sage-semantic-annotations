# -*- coding: utf-8 -*-

from sage.misc.abstract_method import abstract_method
from sage.misc.sage_typing import semantic, ParentOfSelf, Self

@semantic(mmt="Magma", variant="additive")
class AdditiveMagmas:
    class ElementMethods:
        @semantic(mmt=u"∘", gap=r"\+", codomain=ParentOfSelf) #, operator="+")
        @abstract_method
        def _add_(self, other):
            pass

    @semantic(mmt="NeutralElement", variant="additive", gap="IsAdditiveMagmaWithZero")
    class AdditiveUnital:
        class ParentMethods:
            # Defined in NeutralElementLeft
            # - How to retrieve it?
            # - How to detect that this is a method into self?
            @semantic(mmt="neutral", gap="Zero", codomain=Self)
            @abstract_method
            def zero(self):
                # Generates automatically in the XXX.GAP category
                # def zero(self): return self(self.gap().Zero())
                pass

        class ElementMethods:
            @semantic(gap=r"\-", codomain=ParentOfSelf)
            @abstract_method
            def _sub_(self, other):
                # Generates automatically
                # def _sub_(self,other): return self(gap.Subtract(self.gap(), other.gap()))
                pass

            # TODO: Check Additive Inverse
            @semantic(gap="AdditiveInverse", codomain=ParentOfSelf)
            @abstract_method
            def __neg__(self):
                # Generates automatically
                # def _neg_(self): return self.parent()(self.gap().AdditiveInverse())
                pass

    @semantic(gap="IsAdditivelyCommutative")
    class AdditiveCommutative:
        pass
