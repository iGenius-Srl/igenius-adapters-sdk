from random import choice, randint

import factory

from igenius_adapters_sdk.entities import attribute, collection, data, i18n, numeric_binning, params, query, uri

ATTRIBUTE_TYPE_VALUES = [e.value for e in collection.AttributeType]


def create_uid_sequence(name):
    return factory.Sequence(lambda n: f"{name}_uid_{n}")


class AttributeFactory(factory.Factory):
    uid = factory.Sequence(lambda n: f"attr_uid_{n}")
    type = factory.LazyFunction(lambda: choice(ATTRIBUTE_TYPE_VALUES))  # noqa: A003
    filterable = factory.LazyFunction(lambda: choice([True, False]))
    sortable = factory.LazyFunction(lambda: choice([True, False]))

    class Meta:
        model = collection.Attribute


class AttributesSchemaFactory(factory.Factory):
    attributes = factory.LazyFunction(lambda: AttributeFactory.build_batch(size=3))

    class Meta:
        model = collection.AttributesSchema


class CollectionFactory(factory.Factory):
    uid = factory.Sequence(lambda n: f"coll_uid_{n}")
    attributes_schema = factory.SubFactory(AttributesSchemaFactory)

    class Meta:
        model = collection.Collection


class DatasourceUriFactory(factory.Factory):
    datasource_uid = create_uid_sequence("test_datasource")

    class Meta:
        model = uri.DatasourceUri


class CollectionUriFactory(DatasourceUriFactory):
    collection_uid = create_uid_sequence("test_collection")

    class Meta:
        model = uri.CollectionUri


class AttributeUriFactory(CollectionUriFactory):
    attribute_uid = create_uid_sequence("test_attribute")

    class Meta:
        model = uri.AttributeUri


class JoinPartFactory(factory.Factory):
    from_ = factory.SubFactory(CollectionUriFactory)
    on = factory.SubFactory(AttributeUriFactory)

    class Meta:
        model = query.JoinPart


class JoinFactory(factory.Factory):
    left = factory.SubFactory(JoinPartFactory)
    right = factory.SubFactory(JoinPartFactory)
    type = query.JoinType.INNER  # noqa: A003

    class Meta:
        model = query.Join


class StaticValueAttributeFactory(factory.Factory):
    value = 0
    alias = "starting-point"

    class Meta:
        model = data.StaticValueAttribute


class ProjectionAttributeFactory(factory.Factory):
    attribute_uri = factory.SubFactory(AttributeUriFactory)
    alias = factory.LazyAttribute(lambda o: f"projection_{o.attribute_uri.attribute_uid}")

    class Meta:
        model = data.ProjectionAttribute


class FunctionUriFactory(factory.Factory):
    function_type = "aggregation"
    function_uid = attribute.AggregationFunction.AVG.uid
    function_params = None

    class Meta:
        model = data.FunctionUri


class BinFactory(factory.Factory):
    ge = 0
    lt = 10

    class Meta:
        model = numeric_binning.Bin


class BinningRulesFactory(factory.Factory):
    bins = factory.LazyFunction(lambda: [BinFactory(ge=i * 10, lt=i * 10 + 10) for i in range(3)])

    class Meta:
        model = numeric_binning.BinningRules


class AggregationAttributeFactory(factory.Factory):
    attribute_uri = factory.SubFactory(AttributeUriFactory)
    function_uri = factory.SubFactory(
        factory=FunctionUriFactory,
        function_type="aggregation",
        function_uid=attribute.AggregationFunction.IDENTITY.uid,
        function_params=None,
    )
    alias = factory.LazyAttribute(
        lambda o: "_".join(["aggregation", o.attribute_uri.attribute_uid, o.function_uri.function_uid])
    )

    class Meta:
        model = data.AggregationAttribute


class BinningAttributeFactory(factory.Factory):
    attribute_uri = factory.SubFactory(AttributeUriFactory)
    function_uri = factory.SubFactory(
        factory=FunctionUriFactory,
        function_type="group_by",
        function_uid=attribute.GroupByFunction.IDENTITY.uid,
        function_params=None,
    )
    alias = factory.LazyAttribute(
        lambda o: "_".join(["binning", o.attribute_uri.attribute_uid, o.function_uri.function_uid])
    )

    class Meta:
        model = data.BinningAttribute


class BinningAttributeFactoryWithFunctionParam(BinningAttributeFactory):
    function_uri = factory.SubFactory(
        factory=FunctionUriFactory,
        function_type="group_by",
        function_uid=attribute.GroupByFunction.IDENTITY.uid,
        function_params=BinningRulesFactory(),
    )


class I18nFactory(factory.Factory):
    name = "crystal.topic.test.name"
    description = "crystal.topic.test.description"

    class Meta:
        model = i18n.I18n


class ParamOperationSpecsFactory(factory.Factory):
    uid = create_uid_sequence("test-param-operation")
    i18n = factory.SubFactory(I18nFactory)
    properties_schema = params.OperationSchemas.SINGLE_VALUE.jsonschema

    class Meta:
        model = params.ParamOperationSpecs


class ExpressionFactory(factory.Factory):
    attribute_uri = factory.SubFactory(AttributeUriFactory)
    operator = params.ParamOperation.EQUAL.uid
    value = "mocked_value"

    class Meta:
        model = query.Expression


class MultiExpressionFactory(factory.Factory):
    criteria = query.CriteriaType.AND
    expressions = factory.LazyFunction(lambda: ExpressionFactory.build_batch(size=2))

    class Meta:
        model = query.MultiExpression


class OrderByAttributeFactory(factory.Factory):
    alias = "mocked_alias"
    direction = data.OrderByDirection.ASC

    class Meta:
        model = data.OrderByAttribute


class SelectQueryFactory(factory.Factory):
    from_ = factory.SubFactory(CollectionUriFactory)
    attributes = factory.LazyFunction(lambda: ProjectionAttributeFactory.build_batch(size=2))
    distinct = False
    where = None
    order_by = None

    class Meta:
        model = query.SelectQuery


class AggregationQueryFactory(factory.Factory):
    from_ = factory.SubFactory(CollectionUriFactory)
    aggregations = factory.LazyFunction(lambda: AggregationAttributeFactory.build_batch(size=2))
    where = None
    order_by = None

    class Meta:
        model = query.AggregationQuery


class GroupByQueryFactory(factory.Factory):
    from_ = factory.SubFactory(CollectionUriFactory)
    aggregations = factory.LazyFunction(lambda: AggregationAttributeFactory.build_batch(size=2))
    groups = factory.LazyFunction(lambda: BinningAttributeFactory.build_batch(size=2))
    where = None
    order_by = None
    bin_interpolation = None

    class Meta:
        model = query.GroupByQuery


class ItemFactory(factory.Factory):
    uid = create_uid_sequence("item")
    name = factory.Faker("name")
    weight = factory.Faker("pyfloat", right_digits=2, positive=True, min_value=1, max_value=1000)
    price = factory.Faker("pyfloat", right_digits=2, positive=True, min_value=1, max_value=1000)
    order_uid = None

    class Meta:
        model = dict
        rename = {"order_uid": "order.uid"}


class OrderFactory(factory.Factory):
    uid = create_uid_sequence("order")
    name = factory.Faker("name")
    order_date = factory.Faker("date_time_between", start_date="-2y")
    total = factory.LazyFunction(lambda: randint(0, 10))
    customer_uid = None

    items = factory.LazyAttribute(lambda o: ItemFactory.create_batch(size=randint(1, 4), order_uid=o.uid))

    class Meta:
        model = dict
        rename = {"order_date": "order.date"}


class CustomerFactory(factory.Factory):
    uid = create_uid_sequence("customer")
    name = factory.Faker("name")
    creation = factory.Faker("date_time_between", start_date="-2y")
    country = factory.Faker("country")
    points = factory.LazyFunction(lambda: randint(0, 100))

    orders = factory.LazyAttribute(lambda c: OrderFactory.create_batch(size=randint(1, 10), customer_uid=c.uid))

    class Meta:
        model = dict
