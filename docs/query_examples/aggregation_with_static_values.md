# Aggregation with static values

## Query entity

```python
AggregationQuery(
    from_=CollectionUri(
        datasource_uid='test_datasource_uid_0',
        collection_uid='lineitem'
    ),
    where=None,
    order_by=None,
    limit=None,
    offset=None,
    aggregations=[
        AggregationAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_0',
                collection_uid='lineitem',
                attribute_uid='quantity'
            ),
            alias='aggregation_alias_avg',
            function_uri=FunctionUri(
                function_type='aggregation',
                function_uid='crystal.topics.data.aggregation.avg',
                function_params=None
            )
        ),
        StaticValueAttribute(value='0', alias='starting_point'),
        StaticValueAttribute(value='100', alias='target')
    ]
)
```

## JSON payload

```json
{
  "from_": {
    "datasource_uid": "test_datasource_uid_0",
    "collection_uid": "lineitem"
  },
  "where": null,
  "order_by": null,
  "limit": null,
  "offset": null,
  "aggregations": [
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_0",
        "collection_uid": "lineitem",
        "attribute_uid": "quantity"
      },
      "alias": "aggregation_alias_avg",
      "function_uri": {
        "function_type": "aggregation",
        "function_uid": "crystal.topics.data.aggregation.avg",
        "function_params": null
      }
    },
    {
      "value": "0",
      "alias": "starting_point"
    },
    {
      "value": "100",
      "alias": "target"
    }
  ]
}
```

## SQL query

```sql
SELECT
    AVG("lineitem"."quantity") AS "aggregation_alias_avg",
    0 AS "starting_point",
    100 AS "target"
FROM "lineitem";
```