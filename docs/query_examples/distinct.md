# Distinct

## Query entity

```python
SelectQuery(
    from_=CollectionUri(
        datasource_uid='test_datasource_uid_0',
        collection_uid='item'
    ),
    where=None,
    order_by=None,
    limit=None,
    offset=None,
    attributes=[
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_0',
                collection_uid='item',
                attribute_uid='uid'
            ),
            alias='projection_uid'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_1',
                collection_uid='item',
                attribute_uid='name'
            ),
            alias='projection_name'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_2',
                collection_uid='item',
                attribute_uid='order.uid'
            ),
            alias='projection_order.uid'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_3',
                collection_uid='item',
                attribute_uid='weight'
            ),
            alias='projection_weight'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_4',
                collection_uid='item',
                attribute_uid='price'
            ),
            alias='projection_price'
        )
    ],
    distinct=True,
)
```

## JSON payload

```json
{
  "from_": {
    "datasource_uid": "test_datasource_uid_0",
    "collection_uid": "item"
  },
  "where": null,
  "order_by": null,
  "limit": null,
  "offset": null,
  "attributes": [
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_0",
        "collection_uid": "item",
        "attribute_uid": "uid"
      },
      "alias": "projection_uid"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_1",
        "collection_uid": "item",
        "attribute_uid": "name"
      },
      "alias": "projection_name"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_2",
        "collection_uid": "item",
        "attribute_uid": "order.uid"
      },
      "alias": "projection_order.uid"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_3",
        "collection_uid": "item",
        "attribute_uid": "weight"
      },
      "alias": "projection_weight"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_4",
        "collection_uid": "item",
        "attribute_uid": "price"
      },
      "alias": "projection_price"
    }
  ],
  "distinct": true
}
```

## SQL query

```sql
SELECT
	DISTINCT "item"."uid" AS "projection_uid",
	"item"."name" AS "projection_name",
	"item"."order.uid" AS "projection_order.uid",
	"item"."weight" AS "projection_weight",
	"item"."price" AS "projection_price"
FROM
	"item";
```