import pytest
from pydantic import ValidationError

from tests import factories as shf


@pytest.mark.parametrize('ge, lt', [
    pytest.param(None, None),
    pytest.param(2, 2),
    pytest.param(3, 2),
    pytest.param(1.5, 1.3),
    pytest.param(5, 4.6),
])
def test_bin_validator_raises_for_invalid_bin_values(ge, lt):
    err_msg = 'invalid bin values'
    with pytest.raises(ValueError, match=err_msg):
        shf.BinFactory(ge=ge, lt=lt)


@pytest.mark.parametrize('ge, lt', [
    pytest.param(None, 2),
    pytest.param(None, 3.14),
    pytest.param(3, None),
    pytest.param(2.5, None),
    pytest.param(8, 9),
    pytest.param(25, 89),
])
def test_create_bin_successfully(ge, lt):
    shf.BinFactory(ge=ge, lt=lt)


@pytest.mark.parametrize('bins', [
    pytest.param(None),
    pytest.param([]),
    pytest.param([shf.BinFactory(ge=1, lt=2)]),
])
def test_binning_rules_raises_for_insufficient_bins(bins):
    with pytest.raises(ValidationError):
        shf.BinningRulesFactory(bins=bins)


def test_binning_rules_sorts_bins():
    unsorted_bins = [
        shf.BinFactory(ge=30, lt=40),
        shf.BinFactory(ge=20, lt=25),
        shf.BinFactory(ge=25, lt=30),
    ]
    res = shf.BinningRulesFactory(bins=unsorted_bins)
    assert sorted([x.ge for x in unsorted_bins]) == [x.ge for x in res.bins]


@pytest.mark.parametrize('bins', [
    pytest.param([
        shf.BinFactory(ge=10, lt=None),
        shf.BinFactory(ge=20, lt=30),
    ]),
    pytest.param([
        shf.BinFactory(ge=None, lt=20),
        shf.BinFactory(ge=None, lt=30),
    ]),
    pytest.param([
        shf.BinFactory(ge=None, lt=10),
        shf.BinFactory(ge=None, lt=30),
        shf.BinFactory(ge=40, lt=50),
    ]),
    pytest.param([
        shf.BinFactory(ge=None, lt=10),
        shf.BinFactory(ge=20, lt=None),
        shf.BinFactory(ge=40, lt=50),
    ]),
])
def test_binning_rules_raises_for_invalid_null_values(bins):
    err_msg = 'null values found in prohibited properties'
    with pytest.raises(ValidationError, match=err_msg):
        shf.BinningRulesFactory(bins=bins)


@pytest.mark.parametrize('bins', [
    pytest.param([
        shf.BinFactory(ge=10, lt=20),
        shf.BinFactory(ge=15, lt=30),
    ]),
    pytest.param([
        shf.BinFactory(ge=10, lt=22.2),
        shf.BinFactory(ge=20, lt=30),
        shf.BinFactory(ge=28.6, lt=40),
    ]),
    pytest.param([
        shf.BinFactory(ge=2, lt=4),
        shf.BinFactory(ge=4, lt=7.7),
        shf.BinFactory(ge=7.0, lt=9),
    ]),
])
def test_binning_rules_raises_for_overlapping_values(bins):
    err_msg = 'found overlapping bins'
    with pytest.raises(ValidationError, match=err_msg):
        shf.BinningRulesFactory(bins=bins)


@pytest.mark.parametrize('bins', [
    pytest.param([
        shf.BinFactory(ge=10, lt=20),
        shf.BinFactory(ge=30, lt=40),
    ]),
    pytest.param([
        shf.BinFactory(ge=100.1, lt=200.2),
        shf.BinFactory(ge=300.3, lt=400.4),
    ]),
])
def test_binning_rules_accepts_holes_between_bins(bins):
    shf.BinningRulesFactory(bins=bins)


@pytest.mark.parametrize('bin', [
    pytest.param(shf.BinFactory(ge=10, lt=None)),
    pytest.param(shf.BinFactory(ge=20, lt=40)),
    pytest.param(shf.BinFactory(ge=None, lt=20.3)),
])
def test_bin_string_representation(bin):
    assert str(bin) == str(bin.ge)+"-"+str(bin.lt)
