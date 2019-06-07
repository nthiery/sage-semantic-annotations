class Category_over_base_ring:
    @classmethod
    def an_instance(cls):
        from sage.categories.rings import Rings
        return cls(Rings())
