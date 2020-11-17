import pytest

case = pytest.param


def create_entity_test_suite(factory, cases):
    @pytest.mark.parametrize('attr, input_, expected', cases)
    def test(attr, input_, expected):
        actual = factory(**{attr: input_})
        assert expected == getattr(actual, attr)

    return test
