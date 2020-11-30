# URIs

## Function URI

Informs about the function to be used, its type, and optionally for binning provides parameters.

```python
class FunctionUri(BaseModel):
    function_type: Literal['group_by', 'aggregation']
    function_uid: str
    function_params: Optional[Union[numeric_binning.BinningRules]]
```

## Data source URI

Informs about the data source that is used.

```python
class DatasourceUri(UriModel):
    datasource_uid: DatasourceUid
```

## Collection URI

Informs about the collection that is used.

```python
class CollectionUri(UriModel):
    datasource_uid: DatasourceUid
    collection_uid: CollectionUid
```

## Attribute URI

Informs about the data source, collection, and attribute that is used.

```python
Uid = str

AttributeUid = NewType('AttributeUid', Uid)
CollectionUid = NewType('CollectionUid', Uid)
DatasourceUid = NewType('DatasourceUid', Uid)


class AttributeUri(UriModel):
    datasource_uid: DatasourceUid
    collection_uid: CollectionUid
    attribute_uid: AttributeUid
```
