import inspect
from functools import wraps


class Depends:
    def __init__(self, f, *args, **kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.called = None

    def setup(self):
        self.called = self.f(*self.args, **self.kwargs)
        if inspect.isgenerator(self.called):
            return next(self.called)

        return self.called

    def tear_down(self):
        if inspect.isgenerator(self.called):
            try:
                return next(self.called)
            except StopIteration:
                pass


def inject(f):
    fsig = inspect.signature(f)
    dependencies = [
        (var_name, var_value.default)
        for var_name, var_value in fsig.parameters.items()
        if isinstance(var_value.default, Depends)
    ]

    @wraps(f)
    def wrapper(*args, **kwargs):
        for var_name, dep in dependencies:
            kwargs[var_name] = dep.setup()

        res = f(*args, **kwargs)

        for _, dep in dependencies:
            dep.tear_down()

        return res

    return wrapper
