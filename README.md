# The One API SDK for Python

## Overview:
Python SDK for accessing The One API at https://the-one-api.dev/.

Per the instructions found at https://liblab.com/take-home-project, SDK covers only the **movie** and **quote** endpoints.

## Technical Details:

There is a low-level set of apis that are meant to not quite mirror the existing API, but separate the technical integration with the API from the functional one, which is embodied in the sdk classes `Movie`, `Quote`, `Movies` and `Quotes`.

## Architecture:

## Installation:
To install the SDK, from the root directory of the project, run `pip install .`.
To uninstall the SDK, run `pip uninstall theoneapi`.

## Usage:
```
from theoneapi import sdk

VALID_API_KEY = "***REMOVED***"

api = sdk.TheOneApi(VALID_API_KEY)
options = sdk.RequestOptions(sort="name", filter="name=/Of The/i")
movies = sdk.Movies(api).options

options = sdk.RequestOptions(sort="name", filter="name=/Of The/i")
movies = api.movies(options=options)

```
See the test docs in tests/test_theoneapi.py for additional usage examples.

## Testing:

Run all tests:

    python -m pytest tests/*.py 

Run all tests, show coverage (development):

    pip install --upgrade . && python -m coverage run -m pytest --maxfail=1 tests/*.py && coverage html

Run one specific test:

    pip install --upgrade . && pytest -v tests/test_theoneapi.py::TestTheOneAPI::test_movies_object_limit