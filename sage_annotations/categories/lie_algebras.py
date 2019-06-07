from sage.misc.sage_typing import semantic, List, Sage, Self
from sage.misc.abstract_method import abstract_method
from sage.categories.category_with_axiom import CategoryWithAxiom

# TODO: Check the consistency with Sage's LieAlgebras category:
# product denoted by * or ???
from sage.categories.magmatic_algebras import MagmaticAlgebras
# This should be gap_super="IsJacobianRing", and we would need to
# recover the other filters "IsLieAlegbra" is composed of.  This will
# do for now
@semantic(mmt="LieAlgebra", gap="IsJacobianRing")
class LieAlgebras:
    r"""
    A class for Lie algebras.

    The implementation is as handles to GAP objects.

    EXAMPLE::

        sage: from mmt import LieAlgebras
        sage: L = LieAlgebras(Rings()).GAP().example()
        sage: L
        <Lie algebra over Rationals, with 2 generators>
        sage: L.category()
        Category of finite dimensional g a p lie algebras with basis over rings
        sage: Z = L.lie_center()
        sage: Z
        <Lie algebra of dimension 0 over Rationals>
        sage: Z.category()
        Category of finite finite dimensional commutative associative g a p lie algebras with basis over rings
        sage: L     # we know more after computing the center!
        <Lie algebra of dimension 3 over Rationals>
        sage: CZ = L.lie_centralizer(Z)
        sage: CZ
        <Lie algebra of dimension 3 over Rationals>
        sage: CZ.category()
        Category of finite dimensional g a p lie algebras with basis over rings
        sage: CL = L.lie_centralizer(L)
        sage: CL
        <Lie algebra of dimension 0 over Rationals>
        sage: NL = L.lie_normalizer(L)
        sage: NL
        <Lie algebra of dimension 3 over Rationals>
        sage: NZ = L.lie_normalizer(Z)
        sage: NZ
        <Lie algebra of dimension 3 over Rationals>
        sage: L.lie_derived_subalgebra()
        <Lie algebra of dimension 3 over Rationals>
        sage: L.lie_nilradical()
        <Lie algebra of dimension 0 over Rationals>
        sage: L.lie_solvable_radical()
        <Lie algebra of dimension 0 over Rationals>
        sage: L.cartan_subalgebra()
        <Lie algebra of dimension 1 over Rationals>
        sage: L.lie_derived_series()
        [<Lie algebra of dimension 3 over Rationals>]
        sage: L.lie_derived_series()[0]
        <Lie algebra of dimension 3 over Rationals>
        sage: L.lie_lower_central_series()
        [<Lie algebra of dimension 3 over Rationals>]
        sage: L.lie_upper_central_series()
        [<Lie algebra over Rationals, with 0 generators>]
        sage: L.is_lie_abelian()
        False
        sage: Z.is_lie_abelian()
        True
        sage: L.is_lie_nilpotent()
        False
        sage: L.is_lie_solvable()
        False
        sage: L.semi_simple_type()
        'A1'
        sage: L.chevalley_basis()
        [ [ LieObject( [ [ 0, 1 ], [ 0, 0 ] ] ) ],
          [ LieObject( [ [ 0, 0 ], [ 1, 0 ] ] ) ],
          [ LieObject( [ [ 1, 0 ], [ 0, -1 ] ] ) ] ]
        sage: L.root_system()
        <mygap.GAPObject object at 0x...>
        sage: L.root_system().gap()
        <root system of rank 1>
        sage: L.is_restricted_lie_algebra()
        False
    """
    def super_categories(self):
        """
        EXAMPLES::

            sage: from mmt import LieAlgebras
            sage: LieAlgebras(Rings()).super_categories()
            [Category of magmatic algebras over rings]
        """
        return [MagmaticAlgebras(self.base_ring())]

    class ParentMethods:

        @semantic(mmt="TODO", gap="GeneratorsOfAlgebra", codomain=List[Self]) # TODO: tuple_of_self
        @abstract_method
        def lie_algebra_generators(self):
            r"""
            Return generators for this Lie algebra.

            OUTPUT:

                A tuple of elements of ``self``

            EXAMPLES::

                sage: from mmt import LieAlgebras
                sage: L = LieAlgebras(Rings()).GAP().example()
                sage: a, b = L.lie_algebra_generators()
                sage: a, b
                (LieObject( [ [ 0, 1 ],
                              [ 0, 0 ] ] ),
                 LieObject( [ [ 0, 0 ],
                              [ 1, 0 ] ] ))
            """
            # return tuple(self(handle) for handle in self.gap().GeneratorsOfAlgebra())
            pass

        @semantic(mmt="TODO", gap="LieCentre") # TODO: codomain
        def lie_center(self):
            pass

        @semantic(mmt="TODO", gap="LieCentralizer") # TODO: codomain
        def lie_centralizer(self, S):
            pass

        @semantic(mmt="TODO", gap="LieNormalizer") # TODO: codomain
        def lie_normalizer(self, U):
            pass

        @semantic(mmt="TODO", gap="LieDerivedSubalgebra") # TODO: codomain
        def lie_derived_subalgebra():
            pass

        @semantic(mmt="TODO", gap="LieNilRadical") # TODO: codomain
        def lie_nilradical():
            pass

        @semantic(mmt="TODO", gap="LieSolvableRadical") # TODO: codomain
        def lie_solvable_radical():
            pass

        @semantic(mmt="TODO", gap="CartanSubalgebra") # TODO: codomain
        def cartan_subalgebra():
            pass

        @semantic(mmt="TODO", gap="LieDerivedSeries", codomain=List)
        def lie_derived_series():
            pass

        @semantic(mmt="TODO", gap="LieLowerCentralSeries", codomain=List)
        def lie_lower_central_series():
            pass

        @semantic(mmt="TODO", gap="LieUpperCentralSeries", codomain=List)
        def lie_upper_central_series():
            pass

        @semantic(mmt="TODO", gap="IsLieAbelian", codomain=bool)
        def is_lie_abelian():
            pass

        @semantic(mmt="TODO", gap="IsLieNilpotent", codomain=bool)
        def is_lie_nilpotent():
            pass

        @semantic(mmt="TODO", gap="IsLieSolvable", codomain=bool)
        def is_lie_solvable():
            pass

        @semantic(mmt="TODO", gap="SemiSimpleType", codomain=Sage)
        def semi_simple_type():
            pass

        # TODO: so far the 2 following methods return GAP objects

        @semantic(mmt="TODO", gap="ChevalleyBasis") # TODO: codomain
        def chevalley_basis():
            pass

        @semantic(mmt="TODO", gap="RootSystem") # TODO: codomain
        def root_system():
            pass

        @semantic(mmt="TODO", gap="IsRestrictedLieAlgebra", codomain=bool)
        def is_restricted_lie_algebra():
            pass

    class ElementMethods:
        pass

    class GAP(CategoryWithAxiom):
        def example(self):
            r"""
            Return an example of Lie algebra.

            EXAMPLE::

                sage: from mmt import LieAlgebras
                sage: LieAlgebras(Rings()).GAP().example()
                <Lie algebra over Rationals, with 2 generators>
            """
            from mygap import mygap
            from sage.matrix.constructor import matrix
            from sage.rings.rational_field import QQ
            a = matrix([[0, 1],
                        [0, 0]])
            b = matrix([[0, 0],
                        [1, 0]])
            return mygap.LieAlgebra( QQ, [a, b] )
