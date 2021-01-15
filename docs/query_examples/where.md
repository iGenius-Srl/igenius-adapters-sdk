# Where

## Query entity

```python
SelectQuery(
    from_=CollectionUri(
        datasource_uid='test_datasource_uid_0',
        collection_uid='customer'
    ),
    where=Expression(
        attribute_uri=AttributeUri(
            datasource_uid='test_datasource_uid_5',
            collection_uid='customer',
            attribute_uid='uid'
        ),
        operator=ParamOperation.EQUAL.uid,
        value={'data': 'customer_uid_0'}
    ),
    order_by=None,
    limit=None,
    offset=None,
    attributes=[
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_0',
                collection_uid='customer',
                attribute_uid='uid'
            ),
            alias='alias_uid'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_1',
                collection_uid='customer',
                attribute_uid='name'
            ),
            alias='alias_name'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_2',
                collection_uid='customer',
                attribute_uid='creation'
            ),
            alias='alias_creation'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_3',
                collection_uid='customer',
                attribute_uid='country'
            ),
            alias='alias_country'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_4',
                collection_uid='customer',
                attribute_uid='points'),
            alias='alias_points'
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
  "where": {
    "attribute_uri": {
      "datasource_uid": "test_datasource_uid_5",
      "collection_uid": "customer",
      "attribute_uid": "uid"
    },
    "operator": "crystal.topics.data.param-operation.equal",
    "value": {
      "data": "customer_uid_0"
    }
  },
  "order_by": null,
  "limit": null,
  "offset": null,
  "attributes": [
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_0",
        "collection_uid": "customer",
        "attribute_uid": "uid"
      },
      "alias": "alias_uid"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_1",
        "collection_uid": "customer",
        "attribute_uid": "name"
      },
      "alias": "alias_name"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_2",
        "collection_uid": "customer",
        "attribute_uid": "creation"
      },
      "alias": "alias_creation"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_3",
        "collection_uid": "customer",
        "attribute_uid": "country"
      },
      "alias": "alias_country"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_4",
        "collection_uid": "customer",
        "attribute_uid": "points"
      },
      "alias": "alias_points"
    }
  ],
  "distinct": false
}
```

## SQL query

```sql
SELECT
	"customer"."uid" AS "alias_uid",
	"customer"."name" AS "alias_name",
	"customer"."creation" AS "alias_creation",
	"customer"."country" AS "alias_country",
	"customer"."points" AS "alias_points"
FROM
	"customer"
WHERE
	LOWER("customer"."uid")= LOWER('customer_uid_0');
```