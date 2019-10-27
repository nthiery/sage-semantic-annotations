
nested_classes = {
    "elements": "ElementMethods",
    "parents": "ParentMethods",
    "morphisms": "MorphismMethods",
}

class Category:

    def collect_semantic(self):
        semantic = dict(getattr(self, "_semantic", {}))
        for name in nested_classes.keys():
            semantic[name] = semantic.get(name, {})
        for C in self.super_categories():
            C_semantic = C.collect_semantic()
            for name in nested_classes.keys():
                # Could warn if some entry is redefined; this should not happen, right?
                semantic[name].update(C_semantic[name])
        # Update
        for name, clsname in nested_classes.items():
            cls = getattr(self,clsname, None)
            if cls is None:
                continue
            # Could warn if some entry is redefined; this should not happen, right?
            semantic[name].update(getattr(cls, "_semantic", {}))
        return semantic

    def _latex_(self):
        return r"\mathbf{\text{%s}}"%(self._repr_object_names())
