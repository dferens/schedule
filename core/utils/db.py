class QuerySetMixin(object):

    def get_or_prepare(self, defaults=None, **kwargs):
        """
        Looks up an object with the given kwargs, preparing one if necessary.
        Returns a tuple of (object, prepared), where prepared is a boolean
        specifying whether an object was constructed.
        """
        lookup, params = self._extract_model_params(defaults, **kwargs)
        try:
            return self.get(**lookup), False
        except self.model.DoesNotExist:
            obj = self.model(**params)
            return obj, True
