# Join projection

## Query entity

```python
SelectQuery(
    from_=Join(
        left=JoinPart(
            from_=CollectionUri(
                datasource_uid='test_datasource_uid_0',
                collection_uid='customer'
            ),
            on=AttributeUri(
                datasource_uid='test_datasource_uid_0',
                collection_uid='customer',
                attribute_uid='uid'
            )
        ),
        right=JoinPart(
            from_=CollectionUri(
                datasource_uid='test_datasource_uid_1',
                collection_uid='order'
            ),
            on=AttributeUri(
                datasource_uid='test_datasource_uid_1',
                collection_uid='order',
                attribute_uid='customer_uid'
            )
        ),
        type=JoinType.INNER
    ),
    where=None,
    order_by=None,
    limit=None,
    offset=None,
    attributes=[
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_2',
                collection_uid='customer',
                attribute_uid='uid'
            ),
            alias='alias_customer_uid'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_3',
                collection_uid='customer',
                attribute_uid='name'
            ),
            alias='alias_customer_name'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_4',
                collection_uid='order',
                attribute_uid='uid'
            ),
            alias='alias_order_uid'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_5',
                collection_uid='order',
                attribute_uid='date'
            ),
            alias='alias_order_date'
        ),
        ProjectionAttribute(
            attribute_uri=AttributeUri(
                datasource_uid='test_datasource_uid_6',
                collection_uid='order',
                attribute_uid='amount'
            ),
            alias='alias_order_amount'
        )
    ],
    distinct=False
)
```

## JSON payload

```json
{
  "from_": {
    "left": {
      "from_": {
        "datasource_uid": "test_datasource_uid_0",
        "collection_uid": "customer"
      },
      "on": {
        "datasource_uid": "test_datasource_uid_0",
        "collection_uid": "customer",
        "attribute_uid": "uid"
      }
    },
    "right": {
      "from_": {
        "datasource_uid": "test_datasource_uid_1",
        "collection_uid": "order"
      },
      "on": {
        "datasource_uid": "test_datasource_uid_1",
        "collection_uid": "order",
        "attribute_uid": "customer_uid"
      }
    },
    "type": "inner"
  },
  "where": null,
  "order_by": null,
  "limit": null,
  "offset": null,
  "attributes": [
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_2",
        "collection_uid": "customer",
        "attribute_uid": "uid"
      },
      "alias": "alias_customer_uid"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_3",
        "collection_uid": "customer",
        "attribute_uid": "name"
      },
      "alias": "alias_customer_name"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_4",
        "collection_uid": "order",
        "attribute_uid": "uid"
      },
      "alias": "alias_order_uid"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_5",
        "collection_uid": "order",
        "attribute_uid": "date"
      },
      "alias": "alias_order_date"
    },
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_6",
        "collection_uid": "order",
        "attribute_uid": "amount"
      },
      "alias": "alias_order_amount"
    }
  ],
  "distinct": false
}
```

SQL query

```sql
SELECT
	"customer"."uid" AS "alias_customer_uid",
	"customer"."name" AS "alias_customer_name",
	"order"."uid" AS "alias_order_uid",
	"order"."date" AS "alias_order_date",
	"order"."amount" AS "alias_order_amount"
FROM
	( "customer"
INNER JOIN "order" ON
	("customer"."uid" = "order"."customer_uid"));
```