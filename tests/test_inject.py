import asyncio

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

    @inject
    async def func3(d=Depends(dependency, 1)):
        return d

    assert asyncio.run(func3()) == (1, 1)
    assert asyncio.run(func3()) == (1, 1)

    @inject
    async def func4(d=Depends(dependency, 2, b=2)):
        return d

    assert asyncio.run(func4()) == (2, 2)
    assert asyncio.run(func4()) == (2, 2)


reseted = False


def test_generator():
    global reseted

    def dependency():
        global reseted

        yield 1
        reseted = True

    @inject
    def sync_func(d=Depends(dependency)):
        return d

    assert sync_func() == 1
    assert reseted

    reseted = False

    @inject
    async def async_func(d=Depends(dependency)):
        return d

    assert asyncio.run(async_func()) == 1
    assert reseted
