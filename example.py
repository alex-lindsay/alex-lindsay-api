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