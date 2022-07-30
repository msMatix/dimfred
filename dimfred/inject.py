import inspect
from functools import wraps


def inject(f):
    dependencies = Dependencies(f)
    # returns sync / async wrapper based on f
    return dependencies.wrapper()


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


class Dependencies:
    def __init__(self, f):
        self.f = f
        fsig = inspect.signature(f)
        self.dependencies = [
            (var_name, var_value.default)
            for var_name, var_value in fsig.parameters.items()
            if isinstance(var_value.default, Depends)
        ]

    def wrapper(self):
        if inspect.iscoroutinefunction(self.f):
            return self._async_wrapper()

        return self._sync_wrapper()

    def _sync_wrapper(self):
        @wraps(self.f)
        def wrapper(*args, **kwargs):
            self._setup(kwargs)
            try:
                res = self.f(*args, **kwargs)
            except:
                raise
            finally:
                self._tear_down()

            return res

        return wrapper

    def _async_wrapper(self):
        @wraps(self.f)
        async def wrapper(*args, **kwargs):
            self._setup(kwargs)
            try:
                res = await self.f(*args, **kwargs)
            except:
                raise
            finally:
                self._tear_down()

            return res

        return wrapper

    def _setup(self, kwargs):
        for var_name, dep in self.dependencies:
            kwargs[var_name] = dep.setup()

    def _tear_down(self):
        for _, dep in self.dependencies:
            dep.tear_down()
