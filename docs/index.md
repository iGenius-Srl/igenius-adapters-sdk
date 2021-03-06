# iGenius Adapters SDK

This is the Software Development Kit for iGenius Web Connectors development.  
You can use our SDK in your project to be able to handle correctly the data structures that will be used by iGenius services to call your web connector adapter.

## Introduction

### Folder structure

Our SDK has the main objective to expose our data structures that are the business objects of our application: we call them `Entities` and those are included in a package with the same name.
We also provide some `Tools` to automate parts of the processing required by the data structures.

```bash
-- src
   |- igenius_adapters_sdk
      |- entities
      |- tools
```

### Data structure

Our datasource adapters system is based on a relational database structure, so our `entities` are a mapping of this kind of data organisation.

## Install

With Poetry

```bash
poetry add igenius-adapters-sdk
```

With pip

```bash
pip install igenius-adapters-sdk
```
## Further configuration

It is possible to control the behavior of this SDK through environment variables. The currently supported variables are:

- `IGENIUS_ADAPTER_SDK_RE_MATCH_COLLECTION_NAME`:
   specifies the regular expression to check against collection names. The default is `^\S+$` (matches any string not containing spaces, tabs, or line breaks)
