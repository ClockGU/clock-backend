class BaseValidator:
    def __init__(self, data, for_model, instance=None):
        self._data = data
        self._instance = instance
        self._for_model = for_model

    @property
    def data(self):
        return self._data

    @property
    def instnace(self):
        return self._data

    @property
    def for_model_name(self):
        return type(self._for_model).__name__.lower()

    def validate(self):
        try:
            model_validation_method = getattr(
                self, f"get_{self.for_model_name}_validate"
            )
        except AttributeError:
            raise NotImplementedError(
                f"Validation is not implemented for {self.for_model_name} model."
            )
        return model_validation_method()
