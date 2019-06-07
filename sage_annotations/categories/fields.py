from sage.misc.abstract_method import abstract_method
from sage.misc.sage_typing import semantic, Sage

@semantic()
class Fields:
    @semantic(gap="Characteristic", codomain=Sage)
    @abstract_method
    def characteristic(self):
        pass
