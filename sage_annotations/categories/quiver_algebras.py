"""
Tests in this file rely on GAP's QPA package

    sage: from mygap import mygap
    sage: mygap.LoadPackage("qpa")
    ...true
"""

from sage.misc.sage_typing import semantic, List, Sage, Self, Family
from sage.misc.abstract_method import abstract_method
from sage.categories.category_singleton import Category_singleton
from sage.categories.category_types import Category_over_base_ring
from sage.categories.category_with_axiom import CategoryWithAxiom
from sage.categories.semigroups import Semigroups
from sage.categories.algebras import Algebras

@semantic(mmt="Quiver", gap="IsQuiver")
class Quivers(Category_singleton):
    def super_categories(self):
        return [Semigroups()]

    class ParentMethods:
        @semantic(gap="VerticesOfQuiver", codomain=List[Self])
        def vertices(self):
            pass

        @semantic(gap="ArrowsOfQuiver", codomain=List[Self])
        def arrows(self):  # or edges?
            pass

    class GAP(CategoryWithAxiom):

        class ParentMethods:

            def path_algebra(self, base_ring):
                from mygap import mygap
                return mygap.PathAlgebra(base_ring, self)

@semantic(mmt="QuiverAlgebra", gap="IsQuiverAlgebra")
class QuiverAlgebras(Category_over_base_ring):
    r"""
    A class for Quiver algebras.

    TODO: move here the content of the notebook
    """
    def super_categories(self):
        """
        EXAMPLES::

            sage: import mygap
            sage: LieAlgebras(Rings()).super_categories()
            [Category of magmatic algebras over rings]
        """
        return [Algebras(self.base_ring())]

    class ParentMethods:

        @semantic(mmt="TODO", gap="GeneratorsOfAlgebra", codomain=Family[Self]) # TODO: tuple_of_self
        @abstract_method
        def algebra_generators(self):
            r"""
            Return generators for this algebra.

            OUTPUT:

                A tuple of elements of ``self``

            EXAMPLES::

                sage: from sage.categories.quiver_algebras import QuiverAlgebras
                sage: Q = QuiverAlgebras(Rings()).GAP().example()
                sage: v1, a, b = Q.algebra_generators()
                sage: v1, a, b
                ((1)*v1, (1)*a, (1)*b)
            """
            # return tuple(self(handle) for handle in self.gap().GeneratorsOfAlgebra())
            pass

    class GAP(CategoryWithAxiom):
        def example(self):
            r"""
            Return an example of GAP Quiver algebra.

            EXAMPLE::

                sage: from sage.categories.quiver_algebras import QuiverAlgebras
                sage: QuiverAlgebras(Rings()).GAP().example()
                <Rationals[<quiver with 1 vertices and 2 arrows>]>
            """
            from mygap import mygap
            Q = mygap.Quiver( 1, [ [1,1,"a"], [1,1,"b"] ] );
            from sage.rings.rational_field import QQ
            return Q.path_algebra(QQ)
