# The One API SDK for Python

## Overview:
Python SDK for accessing The One API at https://the-one-api.dev/.

Per the instructions found at https://liblab.com/take-home-project, SDK covers only the **movie** and **quote** endpoints.

## Technical Details:

There is a low-level set of apis that are meant to not quite mirror the existing API, but separate the technical integration with the API from the functional one, which is embodied in the sdk classes `Movie`, `Quote`, `Movies` and `Quotes`.

https://the-one-api.dev imposes a rate limit of 100 calls per hour so it's easy to end up butting up against that limit.
It appears that the api returns a 429 code in that case with a message.
TODO: currently this is not handled well an needs guards to properly address non happy path scenarios.

There is an opportunity to add caching within the SDK architecture so that unnecessary calls to the-one-api can be avoided. Given that the api is relatively stable, it'd be save to save that for a relatively long TTL. A cache store like REDIS could be integrated in the base classes

## Architecture:

Type Hinting is used to help ensure that internal consistency is managed, given Python's loose typing.

Fundamentally relatively straightforward, this SDK uses few supporting packages:
`typing` is used to provide a Union type which is utilized for some of the filters which can use string, int, or float values.
`abc` is used to help protect the AbstractBaseClasses (TheOneApiBase and TheOneApiDocBase) from being able to be directly instantiated. (Untested/unverified)
`enum` is used to provide a SortOrder enumeration to help with readability for the TheOneApiBase.sort method.

## Installation:

To install the SDK, from the root directory of the project, run `pip install .`.
To uninstall the SDK, run `pip uninstall theoneapi`.

## Usage:

You can run `python example.py` from the project to see the sdk in use (once you add a valid API key).

```
from decouple import config
from theoneapi import sdk
from pprint import pprint

VALID_API_KEY = config("THEONEAPI_API_KEY")
print(f"API Key: {VALID_API_KEY}")

api = sdk.TheOneApi(VALID_API_KEY)
options = sdk.RequestOptions(sort="name", filter="name=/Of The/i")
movies = sdk.Movies(api, options).fetch()
for movie in movies.docs:
    pprint(movie.as_dict())
    print(f"Movie: {movie.name}")
    quotes = movie.quotes()

    for quote in quotes.docs[0:10]:
        pprint(quote.as_dict())
        print(f"  Quote: {quote.dialog}")

print("Done.")
```
See the test docs in tests/test_theoneapi.py for additional usage examples.

## Testing:

Run all tests:

    python -m pytest tests/*.py 

Run all tests, show coverage (development):

    pip install --upgrade . && python -m coverage run -m pytest --maxfail=1 tests/*.py && coverage html

Run one specific test:

    pip install --upgrade . && pytest -v tests/test_theoneapi.py::TestTheOneAPI::test_movies_object_limit