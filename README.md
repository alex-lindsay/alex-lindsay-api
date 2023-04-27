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

I made a design choice to migrate the `_id` property provided in the data returned by the API calls to a more overt `id` property, since that id is used for making calls to the detail APIs and is used for the filtering, rather than filtering happening by name (e.g.: the quote document has `movie` and `character` properties that are **ids** representing those objects).

This SDK uses few supporting packages:

* `typing` is used to provide a Union type which is utilized for some of the filters which can use string, int, or float values.
* `abc` is used to help protect the AbstractBaseClasses (TheOneApiBase and TheOneApiDocBase) from being able to be directly instantiated. (Untested/unverified)
* `enum` is used to provide a SortOrder enumeration to help with readability for the TheOneApiBase.sort method.
* `decouple` is used for importing the API_KEY from a .env file for tests and the example file.

I used a two layer approach for the overall design: 

* A low-level technical set of APIs that interact in a fairly close way with the external API.
* A more conceptual set of classes that make use of the technical APIs to fulfill their data requests. 
    * `TheOneApiBase` — an abstract base class
        * provides the query capabilities made available to both *movies* and *quotes* (pagination, sorting, filtering)
        * `docs` element — holds a collection of documents returned and processed by the appropriate low level function
        * `fetch` function — left abstract
        * Delegation — migration of the result data from the low-level function into result objects is delegated to the `TheOneApiDocBase` child classes.
    * `Movies` — derived from `TheOneApiBase`
        * `fetch` - uses the low-level `movies` function to retrieve *movie* documents and creates a docs collection internally, delegating the migration of a *movie* data doc to the `Movie` class.
        * `by_id` — uses the low-level `movie` function to retrieve a specialized collection of a single *movie* document, delegating the migration of a movie data doc to the `Movie` class.
    * `Quotes` — derived from `TheOneApiBase`
        * `fetch` - uses the low-level `quotes` function to retrieve *quote* documents and creates a docs collection internally, delegating the migration of a *quote* data doc to the `Quote` class.
        * `by_id` — uses the low-level `quote` function to retrieve a specialized collection of a single *quote* document, delegating the migration of a *quote* data doc to the `Movie` class.
    * `TheOneApiDocBase` — an abstract base class
        * provides an abstraction layer for the data structures underlying both a *movie* and a *quote*
        * `__getitem__` — allows for accessing document internal members using dict syntax
        * `as_dict` — returns a dict containing the known data members
        * `from_dict` — migrats data from the document provided by a low-level function into the internal data structure
    * `Movie` - a document of *movie* information
        * `quotes` — function which allows for the retrieval of a collection of *quote* documents related to the *movie* in question.
    * `Quote` — a document of *quote* information
        * TODO `movie` — a function which retrieves the related `Movies` collection.
    * `RequestOptions` — provides an interface for managing generalize query properties
        * `url_with_query` — a mechanism for taking a url and appending the proper query string to it based on the options present
    * `SortOrder` — an enumeration of ASCENDING and DESCENDING values to make sort order queries more readable.
    * `TheOneApi` — low-level functions close to the-one-api interface
        * `movies` — query for multiple movies using RequestOptions
        * `movie` — query for a single movie using an id
        * `quotes` — query for multiple quotes using RequestOptions
        * `quote` — query for a single quote using an id
        * `movie_quotes` — query for multiple quotes for a single movie using a movie id and RequestOptions

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

## Version History:

### 0.1.0

* Initial Release
    * Low-Level interface to the following APIs
        * https://the-one-api.dev/v2/movies
        * https://the-one-api.dev/v2/movies/{id}
        * https://the-one-api.dev/v2/quotes
        * https://the-one-api.dev/v2/quotes/{id}
        * https://the-one-api.dev/v2/movies/{id}/quotes
    * Functional API representing
        * Movies collection of Movie documents and querying
        * Movie document
            * Related Quotes
        * Quotes collection of Quote documents and querying
    * Basic Documentation
    * Example Script