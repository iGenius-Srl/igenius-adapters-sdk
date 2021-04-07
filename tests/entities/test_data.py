import pytest

from tests.factories import (
    AggregationAttributeFactory,
    BinningAttributeFactory,
    BinningRulesFactory,
    FunctionUriFactory,
    attribute,
)


@pytest.mark.parametrize(
    "function_type, message",
    [
        pytest.param("aggregation", "Invalid AggregationFunction uid=fake-uid", id="AggregationFunctionType"),
        pytest.param("group_by", "Invalid GroupByFunction uid=fake-uid", id="GroupByFunctionType"),
    ],
)
def test_function_uri_factory_raises_for_invalid_function_uid(function_type, message):
    with pytest.raises(ValueError, match=message):
        FunctionUriFactory(function_type=function_type, function_uid="fake-uid")


def test_binning_attribute_return_value():
    binning_attr = BinningAttributeFactory(
        function_uri=FunctionUriFactory(
            function_type="group_by",
            function_uid=attribute.GroupByFunction.NUMERIC_BINNING.uid,
            function_params=BinningRulesFactory(),
        )
    )

    assert binning_attr is not None
    assert len(binning_attr.function_uri.function_params.bins) > 0


def test_binning_attribute_raise_if_wrong_function_type():
    msg = "Function type should be group_by"
    with pytest.raises(ValueError, match=msg):
        BinningAttributeFactory(
            function_uri=FunctionUriFactory(
                function_type="aggregation",
                function_uid=attribute.AggregationFunction.IDENTITY.uid,
            )
        )


def test_aggregation_attribute_raise_if_wrong_function_type():
    msg = "Function type should be aggregation"
    with pytest.raises(ValueError, match=msg):
        AggregationAttributeFactory(
            function_uri=FunctionUriFactory(
                function_type="group_by",
                function_uid=attribute.GroupByFunction.IDENTITY.uid,
            )
        )
