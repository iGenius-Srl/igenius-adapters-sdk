# Select all

## Query entity

```python
SelectQuery(
    from_=CollectionUri(
        datasource_uid='test_datasource_uid_0',
        collection_uid='table'
    ),
    where=None,
    order_by=None,
    limit=None,
    offset=None,
    attributes=[
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_0',
                collection_uid='table',
                attribute_uid='uid'
            ),
            alias='uid'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_1',
                collection_uid='table',
                attribute_uid='name'
            ),
            alias='name'),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_2',
                collection_uid='table',
                attribute_uid='order_uid'
            ),
            alias='order_uid'),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_3',
                collection_uid='table',
                attribute_uid='customer_uid'
            ),
            alias='customer_uid'
        ),
    ],
    distinct=False,
)
```

## JSON payload

```json
{
  "from_": {
    "datasource_uid": "test_datasource_uid_0",
    "collection_uid": "table"
  },
  "where": null,
  "order_by": null,
  "limit": null,
  "offset": null,
  "attributes": [
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_0",
        "collection_uid": "table",
        "attribute_uid": "uid"
      },
      "alias": "uid"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_1",
        "collection_uid": "table",
        "attribute_uid": "name"
      },
      "alias": "name"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_2",
        "collection_uid": "table",
        "attribute_uid": "order_uid"
      },
      "alias": "order_uid"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_3",
        "collection_uid": "table",
        "attribute_uid": "customer_uid"
      },
      "alias": "customer_uid"
    }
  ],
  "distinct": false
}
```

## SQL query

```sql
SELECT
	"table"."uid" AS "uid",
	"table"."name" AS "name",
	"table"."order_uid" AS "order_uid",
	"table"."customer_uid" AS "customer_uid",
FROM
	"table";
```