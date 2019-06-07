import sage.misc.sage_typing as typing
from sage.misc.sage_typing import semantic
from sage.misc.abstract_method import abstract_method

@semantic(mmt="Modules")
class Modules:
    @semantic(gap="IsFreeLeftModule") # TODO: check that this is exactly equivalent
    class WithBasis:
        @semantic(gap="IsFiniteDimensional")
        class FiniteDimensional:
            class ParentMethods:
                @semantic(gap="Dimension", codomain=typing.Sage)
                @abstract_method # FIXME: this overrides ModulesWithBasis.ParentMethods.dimension
                def dimension(self):
                    pass

                # TODO: find an idiom when you want to specify the semantic of
                # a method in a subcategory of where it's defined, and don't
                # want to override the original
                @semantic(gap="Basis", codomain=typing.Family[typing.Self])
                @abstract_method
                def basis_disabled(self):
                    pass
