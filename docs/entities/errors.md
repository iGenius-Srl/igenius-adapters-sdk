# Errors

Errors entities are used to handle error messages towards the client.

## Error payload

Defines the format of the error payload.

```python
class ErrorObject(BaseModel):
    type: str
    message: Union[str, List, Mapping]


class ErrorPayload(BaseModel):
    error: ErrorObject
```
