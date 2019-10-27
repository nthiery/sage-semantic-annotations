from sage.misc.abstract_method import abstract_method
from sage.misc.sage_typing import semantic, Facade, Any

@semantic()
class FiniteGroups:

    class ParentMethods:

        def cardinality(self):
            """
            Returns the cardinality of ``self``, as per
            :meth:`EnumeratedSets.ParentMethods.cardinality`.

            This default implementation calls :meth:`.order` if
            available, and otherwise resorts to
            :meth:`._cardinality_from_iterator`. This is for backward
            compatibility only. Finite groups should override this
            method instead of :meth:`.order`.

            EXAMPLES:

            We need to use a finite group which uses this default
            implementation of cardinality::

                sage: G = groups.misc.SemimonomialTransformation(GF(5), 3); G
                Semimonomial transformation group over Finite Field of size 5 of degree 3
                sage: G.cardinality.__module__
                'sage.categories.finite_groups'
                sage: G.cardinality()
                384
            """
            try:
                o = self.order
            except AttributeError:
                from sage.categories.groups import Groups
                return super(Groups().Finite().parent_class, self).cardinality()
            else:
                return o()

        @semantic(gap="CharacterTable")
        @abstract_method
        def character_table(self):
            """Return the character table of self"""

        @semantic(gap="IrreducibleRepresentations", codomain=Facade[Any])
        @abstract_method
        def irreducible_representations(self, F):
            """Return the irreducible representations of self"""
