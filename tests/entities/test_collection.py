from types import SimpleNamespace
from uuid import uuid4

import pytest
from pydantic import ValidationError

from igenius_adapters_sdk.entities.collection import Attribute, AttributesSchema, AttributeType
from tests import factories

# ATTRIBUTE


@pytest.mark.parametrize("value", ["foobar", "666", 666, str(uuid4())])
def test_create_attribute_with_valid_uid(attribute_factory, value):
    result = attribute_factory(uid=value)
    assert result.uid == str(value)


@pytest.mark.parametrize("value", [e.value for e in AttributeType])
def test_create_attribute_with_valid_type(attribute_factory, value):
    result = attribute_factory(type=value)
    assert result.type == AttributeType(value)


@pytest.mark.parametrize(
    "attr, value",
    [
        pytest.param("uid", None, id="missing uid"),
        pytest.param("uid", SimpleNamespace(uid="ciao"), id="invalid uid"),
        pytest.param("type", None, id="missing type"),
        pytest.param("type", "crystal.topics.data.foobar", id="invalid type"),
    ],
)
def test_create_attribute_fails_for_invalid_params(attribute_factory, attr, value):
    with pytest.raises(ValidationError):
        attribute_factory(**{attr: value})


# ATTRIBUTES SCHEMA


def test_create_empty_attributes_schema(attributes_schema_factory):
    result = attributes_schema_factory(attributes=[])
    assert result.attributes == []


@pytest.mark.parametrize(
    "items",
    [
        pytest.param(list()),
        pytest.param([factories.AttributeFactory()]),
        pytest.param(factories.AttributeFactory.create_batch(2)),
        pytest.param(
            [
                {
                    "uid": "dict-uid",
                    "type": AttributeType.CATEGORICAL,
                    "filterable": True,
                    "sortable": True,
                }
            ]
        ),
        pytest.param(
            [
                {
                    "uid": "has.dot",
                    "type": AttributeType.NUMERIC,
                    "filterable": True,
                    "sortable": True,
                }
            ]
        ),
    ],
)
def test_create_valid_attributes_schema(attributes_schema_factory, items):
    result = attributes_schema_factory(attributes=items)
    assert isinstance(result.attributes, list)
    assert all(isinstance(item, Attribute) for item in result.attributes)


@pytest.mark.parametrize(
    "items",
    [
        pytest.param(None),
        pytest.param([dict(foo="bar")]),
        pytest.param([factories.AttributeFactory(), SimpleNamespace(seh=42)]),
    ],
)
def test_create_invalid_attributes_schema_raises_validation_error(attributes_schema_factory, items):
    with pytest.raises(ValidationError):
        attributes_schema_factory(attributes=items)


# COLLECTION


def test_create_collection_with_valid_params(
    attribute_factory,
    attributes_schema_factory,
    collection_factory,
):
    expected_attributes = attribute_factory.build_batch(size=2)
    attributes_schema = attributes_schema_factory(attributes=expected_attributes)
    result = collection_factory(uid="123", attributes_schema=attributes_schema)
    assert isinstance(result.attributes_schema, AttributesSchema)
    assert result.attributes_schema.attributes == expected_attributes
