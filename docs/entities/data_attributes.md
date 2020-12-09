# Data attributes

Data attributes are the entities needed to describe ordering, static values and generic attributes. All the described entities are available in the `igenius_adapters_sdk.entities.data`.

## Order attribute

Determines the order of the result data if provided.

```python
class OrderByDirection(str, Enum):
    DESC = 'desc'
    ASC = 'asc'

class OrderByAttribute(BaseModel):
    alias: str
    direction: OrderByDirection = OrderByDirection.ASC
```

## Static value

Provides raw data from an attribute.

```python
class StaticValueAttribute(BaseModel):
    value: str
    alias: str
```

## Base attribute

Attribute model that is followed by Aggregation and GroupBy Attribute.

```python
class BaseAttribute(BaseModel, abc.ABC):
    attribute_uri: uri.AttributeUri
    alias: str
```

## Aggregation attribute

Provides aggregated data as a result.

```python
class AggregationAttribute(BaseAttribute):
    function_uri: FunctionUri
```

## Binning attribute

Provides binned data as a result.

```python
class BinningAttribute(BaseAttribute):
    function_uri: FunctionUri
```
