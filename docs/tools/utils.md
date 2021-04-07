# Utils

## bin_interpolation
`(query: GroupByQuery, result: List[Mapping]) -> List[Mapping]`

* `query`: the starting query
* `result`: the result on which aplying the bin interpolation

This function returns the result of a binned [`GroupBy`](../entities/queries.md#groupby-query) query, including the potentially missing bins resulting from the combinations of [`BinningAttribute`](../entities/data_attributes.md#binning-attribute) used in `group` parameter. For such empty bins, the [`default_bin_interpolation`](../entities/data_attributes.md#aggregation-attribute) parameter of the aggregation attiributes allow to specify the value to use (`None` value will be used if not specified).


```python
from igenius_adapters_sdk.tools.utils import bin_interpolation
...

    result = my_own_query_engine(group_by_query)
    if group_by_query.bin_interpolation is True:
        result = bin_interpolation(group_by_query, result)
    return result
```