# Order by

## Query entity

```python
SelectQuery(
    from_=CollectionUri(
        datasource_uid='test_datasource_uid_0',
        collection_uid='customer'
    ),
    where=None,
    order_by=[
        OrderByAttribute(
            alias='uid',
            direction=OrderByDirection.ASC
        )
    ],
    limit=None,
    offset=None,
    attributes=[
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_0',
                collection_uid='customer',
                attribute_uid='uid'
            ),
            alias='projection_uid'
        )
    ],
    distinct=False,
)
```

## JSON payload

```json
{
  "from_": {
    "datasource_uid": "test_datasource_uid_0",
    "collection_uid": "customer"
  },
  "where": null,
  "order_by": [
    {
      "alias": "uid",
      "direction": "asc"
    }
  ],
  "limit": null,
  "offset": null,
  "attributes": [
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_0",
        "collection_uid": "customer",
        "attribute_uid": "uid"
      },
      "alias": "projection_uid"
    }
  ],
  "distinct": false
}
```

## SQL query

```sql
SELECT
	"customer"."uid" AS "projection_uid"
FROM
	"customer"
ORDER BY
	"uid" ASC ;
```