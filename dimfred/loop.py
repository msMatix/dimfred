from functools import wraps


def loop(
    *_,
    times=None,
    result_handler=None,
    exception_handler=lambda f, args, kwargs: f(*args, **kwargs)
):
    """Runs a function in a loop.
    If times!=None, will run the loop N times.
    If results_handler!=None, will apply the function and handle the result.
    """

    def wrapper(f):
        def run(*args, **kwargs):
            res = f(*args, **kwargs)
            if result_handler is not None:
                result_handler(res)

        @wraps(f)
        def deco(*args, **kwargs):
            if times is not None:
                for _ in range(times):
                    exception_handler(run, args, kwargs)
            else:
                while True:
                    exception_handler(run, args, kwargs)

        return deco

    return wrapper
