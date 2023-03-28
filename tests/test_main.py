import pytest as pytest


def test_３の倍数の場合fizzを返す():
    from fizzbuzz.main import fizzbuzz
    assert fizzbuzz(3) == 'fizz'


def test_５の倍数の場合buzzを返す():
    from fizzbuzz.main import fizzbuzz
    assert fizzbuzz(5) == 'buzz'


def test_３と５の倍数の場合fizzbuzzを返す():
    from fizzbuzz.main import fizzbuzz
    assert fizzbuzz(15) == 'fizzbuzz'


def test_それ以外の場合はその数字を文字列で返す():
    from fizzbuzz.main import fizzbuzz
    assert fizzbuzz(1) == '1'


def test_数字以外の場合はエラーを返す():
    from fizzbuzz.main import fizzbuzz
    with pytest.raises(TypeError):
        fizzbuzz('a')
