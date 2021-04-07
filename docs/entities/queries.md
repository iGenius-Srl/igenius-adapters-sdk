# Queries

Inform about the data source that is used, query statements, and order.

All queries follow BaseQuery model.

```python
class BaseQuery(BaseModel, abc.ABC):
    from_: From
    where: Optional[WhereExpression]
    order_by: Optional[List[data.OrderByAttribute]]
    limit: int = Field(None, gt=0)
    offset: int = Field(None, ge=0)
```

## Select Query

Fetches simple data.

```python
class SelectQuery(BaseQuery):
    attributes: List[Union[data.ProjectionAttribute, data.StaticValueAttribute]]
    distinct: bool = False
```

## Aggregation Query

Fetches aggregated data.

```python
class AggregationQuery(BaseQuery):
    aggregations: List[Union[data.AggregationAttribute, data.StaticValueAttribute]]
```

## GroupBy Query

Fetches grouped data.

```python
class GroupByQuery(BaseQuery):
    aggregations: List[Union[data.AggregationAttribute, data.StaticValueAttribute]]
    groups: List[data.BinningAttribute],
    bin_interpolation: Optional[bool] = True
```

!!! info
    `bin_interpolation` flag tells whether the result of the query should contain all the bins resulting from the combinations of the attributes used in `groups` parameter, including the empty ones. [`Bin interpolation`](../tools/utils.md#bin_interpolation) utils provides an helper for such cases. The [`default_bin_interpolation`](../entities/data_attributes.md#aggregation-attribute) value specified in the aggregations attributes will be used for the empty bins (`None` value will be used if not specified).
## Query

All used types of queries.

```python
Query = Union[GroupByQuery, AggregationQuery, SelectQuery]
```
