from dimfred import Depends, inject


def test_plain_func():
    def dependency(a, b=1):
        return a, b

    @inject
    def func1(d=Depends(dependency, 1)):
        return d

    assert func1() == (1, 1)
    assert func1() == (1, 1)

    @inject
    def func2(d=Depends(dependency, 2, b=2)):
        return d

    assert func2() == (2, 2)
    assert func2() == (2, 2)


reseted = False


def test_generator():
    def dependency():
        global reseted

        yield 1
        reseted = True

    @inject
    def func(d=Depends(dependency)):
        return d

    assert func() == 1
    assert reseted
