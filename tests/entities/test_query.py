import pytest

from tests.factories import AggregationQueryFactory, GroupByQueryFactory, SelectQueryFactory
from tests.factories import (
    AggregationAttributeFactory,
    JoinFactory,
    ProjectionAttributeFactory,
    BinningAttributeFactory,
    MultiExpressionFactory,
)
from igenius_adapters_sdk.entities.query import Query


class Dummy:
    aggregation_attributes = AggregationAttributeFactory.create_batch(2)
    projection = ProjectionAttributeFactory.create_batch(2)
    binning_attributes = BinningAttributeFactory.create_batch(2)
    from_ = JoinFactory()
    where = MultiExpressionFactory()


class Case:
    From = pytest.param(
        'from_',
        Dummy.from_,
        Dummy.from_,
        id='from_'
    )
    Attributes = pytest.param(
        'attributes',
        Dummy.projection,
        Dummy.projection,
        id='attributes'
    )
    Aggregations = pytest.param(
        'aggregations',
        Dummy.aggregation_attributes,
        Dummy.aggregation_attributes,
        id='aggregations'
    )
    Groups = pytest.param(
        'groups',
        Dummy.binning_attributes,
        Dummy.binning_attributes,
        id='groups'
    )
    Distinct = pytest.param(
        'distinct',
        False,
        False,
        id='distinct'
    )
    Where = pytest.param(
        'where',
        Dummy.where,
        Dummy.where,
        id='where'
    )


def create_entity_test_suite(factory, cases):
    @pytest.mark.parametrize('attr, input_, expected', cases)
    def test(attr, input_, expected):
        actual = factory(**{attr: input_})
        assert expected == getattr(actual, attr)

    return test


def is_instance_of_union_type(union_type, instance) -> bool:
    """ Since it's not possible to runtime check an instance
    against a Union type, this method gets the elements of the union
    and returns true if the instance is of one of those types.
    """
    return any(isinstance(instance, x) for x in union_type.__args__)


test_select_query_has_expected_attribute = create_entity_test_suite(
    SelectQueryFactory,
    [Case.From, Case.Attributes, Case.Distinct, Case.Where]
)

test_aggregation_query_has_expected_attribute = create_entity_test_suite(
    AggregationQueryFactory,
    [Case.From, Case.Aggregations, Case.Where]
)

test_groupby_query_has_expected_attribute = create_entity_test_suite(
    GroupByQueryFactory,
    [Case.From, Case.Aggregations, Case.Groups, Case.Where]
)


@pytest.mark.parametrize('create_instance', [
    pytest.param(SelectQueryFactory, id='SelectQuery'),
    pytest.param(AggregationQueryFactory, id='AggregationQueryFactory'),
    pytest.param(GroupByQueryFactory, id='GroupByQueryFactory'),
])
def test_entity_is_a_query(create_instance):
    assert is_instance_of_union_type(Query, create_instance())
