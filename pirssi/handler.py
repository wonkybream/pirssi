from inspect import signature


class Handler(list):
    """
    A list of callable objects.

    Callable object must accept one positional argument.
    """
    def __call__(self, *args, **kwargs):
        for function in self:
            function(*args, **kwargs)

    def __repr__(self):
        return f"Handler({list.__repr__(self)})"

    def append(self, *args, **kwargs):
        if len(signature(args[0]).parameters) != 1:
            raise AssertionError("Callable object must have only one argument")

        super().append(*args, **kwargs)
