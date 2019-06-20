from sage.misc.sage_typing import semantic

@semantic(mmt="Semigroup", variant="additive", gap="IsNearAdditiveMagma")
class AdditiveSemigroups:
    # Additive Magmas are always assumed to be associative and commutative in GAP
    # Near Additive Magmas don't require commutativity
    # See http://www.gap-system.org/Manuals/doc/ref/chap55.html

    # Note: Additive Magmas are always assumed to be associative and commutative in GAP
    @semantic(gap="IsAdditiveMagma")
    class AdditiveCommutative:
        pass

    # In principle this is redundant with isAdditiveMagmaWithZero
    # specified above; however IsAdditiveMagmaWithZero does not
    # necessarily appear in the categories of an additive gap monoid
    @semantic(gap="IsNearAdditiveMagmaWithZero")
    class AdditiveUnital:
        @semantic(gap="IsNearAdditiveGroup")
        class AdditiveInverse:
            pass
