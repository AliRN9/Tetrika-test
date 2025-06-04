import pytest

from task1.solution import strict


@strict
def add(a: int, b: int) -> int:
    return a + b


@strict
def get_offer(text: str, exclaim: bool) -> str:
    return text.upper() + "!" if exclaim else text


@strict
def multiply(a: float, b: float) -> float:
    return a * b


@strict
def divide(a: float, b: int) -> float:
    return a / b


@strict
def concat(a: str, b: str) -> str:
    return a + b


@strict
def wrong_return(a: int, b: int) -> str:
    return a + b


def test_add_success():
    assert add(1, 2) == 3
    assert add(5, 5) == 10


@pytest.mark.parametrize("b", ["2", 2.5])
def test_add_wrong(b):
    with pytest.raises(TypeError):
        add(1, b)


def test_get_offer_success():
    assert get_offer("i want to receive an offer", True) == "I WANT TO RECEIVE AN OFFER!"


@pytest.mark.parametrize("b", ["2", 2.5, 2])
def test_get_offer_wrong(b):
    with pytest.raises(TypeError):
        get_offer("hi", b)


def test_multiply__success():
    assert multiply(2.0, 3.0) == 6.0


def test_multiply__wrong():
    with pytest.raises(TypeError):
        multiply(2.0, 3)


def test_divide__success():
    assert divide(2.0, 1)


def test_divide__wrong():
    with pytest.raises(TypeError):
        assert divide(2.0, 1.0)


def test_concat__success():
    assert concat("foo", "bar") == "foobar"


def test_concat__wrong():
    with pytest.raises(TypeError):
        concat("foo", 5)


def test_return_type_check__wrong():
    with pytest.raises(TypeError):
        wrong_return(1, 2)
