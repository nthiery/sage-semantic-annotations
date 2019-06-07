from sage.misc.abstract_method import abstract_method
from sage.misc.sage_typing import semantic, Facade, Family, Self
from sage.categories.category import Category
import sage.categories.sets_cat

@semantic(mmt="Semigroup", variant="multiplicative", gap="IsAssociative")
class Semigroups:
    class ParentMethods:
        @semantic(gap="GeneratorsOfSemigroup", codomain=Family[Self])
        @abstract_method
        def semigroup_generators(self):
            pass

        @semantic(gap="\/")
        @abstract_method
        def __truediv__(self, relations):
            pass

        @semantic(gap="IsLTrivial", codomain=bool)
        @abstract_method
        def is_l_trivial(self):
            pass

        @semantic(gap="IsRTrivial", codomain=bool)
        @abstract_method
        def is_r_trivial(self):
            pass

        @semantic(gap="IsDTrivial", codomain=bool)
        @abstract_method
        def is_d_trivial(self):
            pass

    @semantic()
    class Finite:
        class ParentMethods:
            @semantic(gap="GreensJClasses", codomain=Facade[Facade[Self]])
            @abstract_method
            def j_classes(self):
                pass

            @semantic(gap="GreensLClasses", codomain=Facade[Facade[Self]])
            @abstract_method
            def l_classes(self):
                pass

            @semantic(gap="GreensRClasses", codomain=Facade[Facade[Self]])
            @abstract_method
            def r_classes(self):
                pass

            @semantic(gap="GreensDClasses", codomain=Facade[Facade[Self]])
            @abstract_method
            def d_classes(self):
                pass

            @semantic(gap="StructureDescriptionMaximalSubgroups")
            @abstract_method
            def structure_description_maximal_subgroups(self):
                pass

            @semantic(gap="StructureDescriptionSchutzenbergerGroups")
            @abstract_method
            def structure_description_schutzenberger_groups(self):
                pass

            @semantic(gap="IsomorphismTransformationSemigroup")
            @abstract_method
            def isomorphism_transformation_semigroup(self):
                pass

    @semantic(gap="IsMonoidAsSemigroup")
    class Unital:
        class ParentMethods:
            @semantic(gap="GeneratorsOfMonoid", codomain=Family[Self])
            @abstract_method
            def monoid_generators(self):
                pass

        @semantic()
        class Finite:
            class ParentMethods:
                @semantic(gap="IsomorphismTransformationMonoid")
                @abstract_method
                def isomorphism_transformation_monoid(self):
                    pass

    @semantic(gap="IsGreensClass")
    class GreensClass(Category):
        def super_categories(self):
            return [sage.categories.sets_cat.Sets()]

        class ParentMethods:
            @semantic(gap="SchutzenbergerGroup")
            def schutzenberger_group(self):
                pass
