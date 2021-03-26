# Chassis

The purpose of this class is to automate all the post processing operations required by the specification of the given query. Currently, the only supported operation is [`Bin interpolation`](../entities/queries.md#groupby-query)

The user needs to provide a callback function where the query is actually executed. The class will take care of performing all the relevant operations defined in the query itself.

```python
from typing import List, Mapping

from igenius_adapters_sdk.tools.chassis import Chassis
from igenius_adapters_sdk.entities.query import Query

...
def my_engine(query: Query) -> List[Mapping]:
    ...
    return my_partial_result
...
ch = Chassis(query, my_engine)
final_result = ch.run()
```
## Chassis.run
Calls the `engine` callback passing the query as paramenter, then apply the required automation on the given result
## Chassis.async_run
Same as `run`, but awaiting for the result of the provided `engine` async callback