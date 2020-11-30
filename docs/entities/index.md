# Entities

`Entities` can be simple Python custom types or Pydantic models. The second option give the great possibility to be able to define our `Entities` using Python code, with great validation capabilities at runtime.

You can use our entities as a contract between our backend services and your datasource connector. In this way you can verify the correctness both of the input and the output of your API endpoint.