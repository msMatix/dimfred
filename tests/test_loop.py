import pytest

from dimfred import loop

counter = 0


def test_okay_loop_runs_times():
    global counter

    counter = 0

    def on_result(c):
        global counter

        assert c == counter
        counter += 1

    @loop(times=3, result_handler=on_result)
    def f():
        global counter

        return counter

    f()


def test_okay_loop_runs_inf():
    global counter

    counter = 0

    def on_result(c):
        global counter

        assert c == counter
        counter += 1

    @loop(result_handler=on_result)
    def f():
        global counter

        if counter < 1000:
            return counter

        raise Exception(counter)

    with pytest.raises(Exception) as e:
        f()

    assert int(str(e.value)) == 1000
