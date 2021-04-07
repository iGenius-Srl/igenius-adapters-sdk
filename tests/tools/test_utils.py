import pytest

from igenius_adapters_sdk.entities import attribute
from igenius_adapters_sdk.tools import utils
from tests import factories as shf


@pytest.mark.parametrize(
    "engine_result, final_result, bins, aggregation_alias",
    [
        pytest.param(
            [
                {"price": "0.0-20.0", "quantity": 140},
                {"price": "21.0-40.0", "quantity": 6634},
                {"price": "40.0-None", "quantity": 135},
            ],
            [
                {"price": "0.0-20.0", "quantity": 140},
                {"price": "20.0-21.0", "quantity": None},
                {"price": "21.0-40.0", "quantity": 6634},
                {"price": "40.0-None", "quantity": 135},
            ],
            {
                "price": [
                    shf.BinFactory(ge=0.0, lt=20.0),
                    shf.BinFactory(ge=20.0, lt=21.0),
                    shf.BinFactory(ge=21.0, lt=40.0),
                    shf.BinFactory(ge=40.0, lt=None),
                ]
            },
            "quantity",
        ),
        pytest.param(
            [
                {"price": "20.0-40.0", "quantity": 15190, "rating": "4.0-NaN"},
                {"price": "40.0-NaN", "quantity": 21257, "rating": "3.0-4.0"},
                {"price": "40.0-NaN", "quantity": 8361, "rating": "0.0-1.0"},
                {"price": "40.0-NaN", "quantity": 1371, "rating": "2.0-3.0"},
                {"price": "20.0-40.0", "quantity": 1031, "rating": "2.0-3.0"},
                {"price": "40.0-NaN", "quantity": 35342, "rating": "4.0-NaN"},
                {"price": "20.0-40.0", "quantity": 3384, "rating": "0.0-1.0"},
                {"price": "0.0-20.0", "quantity": 1068, "rating": "4.0-NaN"},
                {"price": "20.0-40.0", "quantity": 5693, "rating": "3.0-4.0"},
            ],
            [
                {"price": "0.0-20.0", "quantity": None, "rating": "0.0-1.0"},
                {"price": "0.0-20.0", "quantity": None, "rating": "1.0-2.0"},
                {"price": "0.0-20.0", "quantity": None, "rating": "2.0-3.0"},
                {"price": "0.0-20.0", "quantity": None, "rating": "3.0-4.0"},
                {"price": "0.0-20.0", "quantity": 1068, "rating": "4.0-None"},
                {"price": "20.0-40.0", "quantity": 3384, "rating": "0.0-1.0"},
                {"price": "20.0-40.0", "quantity": None, "rating": "1.0-2.0"},
                {"price": "20.0-40.0", "quantity": 1031, "rating": "2.0-3.0"},
                {"price": "20.0-40.0", "quantity": 5693, "rating": "3.0-4.0"},
                {"price": "20.0-40.0", "quantity": 15190, "rating": "4.0-None"},
                {"price": "40.0-None", "quantity": 8361, "rating": "0.0-1.0"},
                {"price": "40.0-None", "quantity": None, "rating": "1.0-2.0"},
                {"price": "40.0-None", "quantity": 1371, "rating": "2.0-3.0"},
                {"price": "40.0-None", "quantity": 21257, "rating": "3.0-4.0"},
                {"price": "40.0-None", "quantity": 35342, "rating": "4.0-None"},
            ],
            {
                "price": [
                    shf.BinFactory(ge=0.0, lt=20.0),
                    shf.BinFactory(ge=20.0, lt=40.0),
                    shf.BinFactory(ge=40.0, lt=None),
                ],
                "rating": [
                    shf.BinFactory(ge=0.0, lt=1.0),
                    shf.BinFactory(ge=1.0, lt=2.0),
                    shf.BinFactory(ge=2.0, lt=3.0),
                    shf.BinFactory(ge=3.0, lt=4.0),
                    shf.BinFactory(ge=4.0, lt=None),
                ],
            },
            "quantity",
        ),
    ],
)
def test_bin_interpolation(engine_result, final_result, bins, aggregation_alias):
    query = shf.GroupByQueryFactory(
        bin_interpolation=True,
        aggregations=[shf.AggregationAttributeFactory(alias=aggregation_alias)],
        groups=[
            shf.BinningAttributeFactory(
                alias=b,
                function_uri=shf.FunctionUriFactory(
                    function_type="group_by",
                    function_uid=attribute.GroupByFunction.NUMERIC_BINNING.uid,
                    function_params=shf.BinningRulesFactory(bins=bins[b]),
                ),
            )
            for b in bins
        ],
    )
    assert final_result == utils.bin_interpolation(query, engine_result)


@pytest.mark.parametrize(
    "engine_result, final_result, bins, aggregation",
    [
        pytest.param(
            [
                {"price": "0.0-20.0", "quantity": 140},
                {"price": "21.0-None", "quantity": 135},
            ],
            [
                {"price": "0.0-20.0", "quantity": 140},
                {"price": "20.0-21.0", "quantity": "missing"},
                {"price": "21.0-None", "quantity": 135},
            ],
            {
                "price": [
                    shf.BinFactory(ge=0.0, lt=20.0),
                    shf.BinFactory(ge=20.0, lt=21.0),
                    shf.BinFactory(ge=21.0, lt=None),
                ]
            },
            shf.AggregationAttributeFactory(alias="quantity", default_bin_interpolation="missing"),
        ),
        pytest.param(
            [
                {"price": "0.0-20.0", "quantity": 140},
                {"price": "21.0-None", "quantity": 135},
            ],
            [
                {"price": "0.0-20.0", "quantity": 140},
                {"price": "20.0-21.0", "quantity": 0},
                {"price": "21.0-None", "quantity": 135},
            ],
            {
                "price": [
                    shf.BinFactory(ge=0.0, lt=20.0),
                    shf.BinFactory(ge=20.0, lt=21.0),
                    shf.BinFactory(ge=21.0, lt=None),
                ]
            },
            shf.StaticValueAttributeFactory(alias="quantity", default_bin_interpolation=0),
        ),
    ],
)
def test_bin_interpolation_with_ovewritten_default(engine_result, final_result, bins, aggregation):
    query = shf.GroupByQueryFactory(
        bin_interpolation=True,
        aggregations=[aggregation],
        groups=[
            shf.BinningAttributeFactory(
                alias=b,
                function_uri=shf.FunctionUriFactory(
                    function_type="group_by",
                    function_uid=attribute.GroupByFunction.NUMERIC_BINNING.uid,
                    function_params=shf.BinningRulesFactory(bins=bins[b]),
                ),
            )
            for b in bins
        ],
    )
    assert final_result == utils.bin_interpolation(query, engine_result)
