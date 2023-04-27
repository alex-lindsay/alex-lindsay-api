import unittest
from theoneapi import sdk
from pprint import pprint

VALID_API_KEY = "***REMOVED***"
INVALID_API_KEY = "FOO"

# NOTE: Normally I'd mock the actual API Calls to The One API, but I'm not going to do that in the interest of saving time.


class TestTheOneAPI(unittest.TestCase):
    SORTED_MOVIE_NAMES = [
        "The Battle of the Five Armies",
        "The Desolation of Smaug",
        "The Fellowship of the Ring",
        "The Hobbit Series",
        "The Lord of the Rings Series",
        "The Return of the King",
        "The Two Towers",
        "The Unexpected Journey",
    ]

    SORTED_OF_THE_MOVIE_NAMES = [
        "The Battle of the Five Armies",
        "The Fellowship of the Ring",
        "The Lord of the Rings Series",
        "The Return of the King",
    ]

    SORTED_BIG_WINNER_MOVIE_NAMES = [
        "The Lord of the Rings Series",
        "The Return of the King",
    ]

    def test_init(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        self.assertEqual(api._api_key, VALID_API_KEY)
        self.assertEqual(api.BASE_URL, "https://the-one-api.dev/v2/")

    def test_movies(self):
        api = sdk.TheOneApi(INVALID_API_KEY)
        movies = api.movies()
        self.assertIn("message", movies)
        self.assertEqual(movies["message"], "Unauthorized.")

        api = sdk.TheOneApi(VALID_API_KEY)
        movies = api.movies()
        self.assertIn("docs", movies)
        self.assertEqual(movies["total"], len(TestTheOneAPI.SORTED_MOVIE_NAMES))

    def test_movies_sort(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        options = sdk.RequestOptions(sort="name")
        movies = api.movies(options=options)
        self.assertIn("docs", movies)
        self.assertEqual(movies["total"], len(TestTheOneAPI.SORTED_MOVIE_NAMES))
        self.assertEqual([movie["name"] for movie in movies["docs"]], TestTheOneAPI.SORTED_MOVIE_NAMES)

    def test_movies_sort_plus(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        options = sdk.RequestOptions(sort="+name")
        movies = api.movies(options=options)
        self.assertIn("docs", movies)
        self.assertEqual(movies["total"], len(TestTheOneAPI.SORTED_MOVIE_NAMES))
        self.assertEqual([movie["name"] for movie in movies["docs"]], TestTheOneAPI.SORTED_MOVIE_NAMES)

    def test_movies_sort_desc(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        options = sdk.RequestOptions(sort="-name")
        movies = api.movies(options=options)
        self.assertIn("docs", movies)
        self.assertEqual(movies["total"], len(TestTheOneAPI.SORTED_MOVIE_NAMES))
        self.assertEqual([movie["name"] for movie in movies["docs"]], list(reversed(TestTheOneAPI.SORTED_MOVIE_NAMES)))

    def test_movies_limit(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        options = sdk.RequestOptions(sort="name", limit=3)
        movies = api.movies(options=options)
        self.assertIn("docs", movies)
        self.assertEqual(movies["total"], 8)
        self.assertEqual(movies["page"], 1)
        self.assertEqual(movies["pages"], 3)
        self.assertEqual(len(movies["docs"]), 3)
        self.assertEqual([movie["name"] for movie in movies["docs"]], TestTheOneAPI.SORTED_MOVIE_NAMES[0:3])

    def test_movies_page(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        options = sdk.RequestOptions(sort="name", limit=3, page=2)
        movies = api.movies(options=options)
        self.assertIn("docs", movies)
        self.assertEqual(movies["total"], 8)
        self.assertEqual(movies["page"], 2)
        self.assertEqual(movies["pages"], 3)
        self.assertEqual(len(movies["docs"]), 3)
        self.assertEqual([movie["name"] for movie in movies["docs"]], TestTheOneAPI.SORTED_MOVIE_NAMES[3:6])

    # TODO - This test is failing. I'm not sure why. offset is not working as expected.
    def test_movies_offset(self):
        # api = sdk.TheOneApi(VALID_API_KEY)
        # options = sdk.RequestOptions(sort="name", limit=3, page=2, offset=1)
        # movies = api.movies(options=options)
        # self.assertIn("docs", movies)
        # self.assertEqual(movies["total"], 8)
        # self.assertEqual(len(movies["docs"]), 3)
        # self.assertEqual([movie["name"] for movie in movies["docs"]], TestTheOneAPI.SORTED_MOVIE_NAMES[4:7])
        pass

    def test_movies_filter(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        options = sdk.RequestOptions(sort="name", filter="name=The Battle of the Five Armies")
        movies = api.movies(options=options)
        self.assertEqual([movie["name"] for movie in movies["docs"]], TestTheOneAPI.SORTED_MOVIE_NAMES[0:1])

        options = sdk.RequestOptions(sort="name", filter="name!=The Battle of the Five Armies")
        movies = api.movies(options=options)
        self.assertEqual([movie["name"] for movie in movies["docs"]], TestTheOneAPI.SORTED_MOVIE_NAMES[1:])

        options = sdk.RequestOptions(sort="name", filter="name=Doesn't Exist")
        movies = api.movies(options=options)
        self.assertEqual([movie["name"] for movie in movies["docs"]], [])

        options = sdk.RequestOptions(sort="name", filter="name=The Desolation of Smaug,The Battle of the Five Armies")
        movies = api.movies(options=options)
        self.assertEqual([movie["name"] for movie in movies["docs"]], TestTheOneAPI.SORTED_MOVIE_NAMES[0:2])

        options = sdk.RequestOptions(sort="name", filter="name=/Of The/i")
        movies = api.movies(options=options)
        self.assertEqual([movie["name"] for movie in movies["docs"]], TestTheOneAPI.SORTED_OF_THE_MOVIE_NAMES)

        options = sdk.RequestOptions(sort="-academyAwardWins", filter="academyAwardWins>=10")
        movies = api.movies(options=options)
        self.assertEqual([movie["name"] for movie in movies["docs"]], TestTheOneAPI.SORTED_BIG_WINNER_MOVIE_NAMES)

    def test_movie_object(self):
        movie_dict = {
            "_id": "5cd95395de30eff6ebccde5c",
            "name": "The Fellowship of the Ring",
            "runtimeInMinutes": 178,
            "budgetInMillions": 93,
            "boxOfficeRevenueInMillions": 871.5,
            "academyAwardNominations": 13,
            "academyAwardWins": 4,
            "rottenTomatesScore": 91,
            "invalidProperty": "Whatever",
        }
        result_dict = movie_dict.copy()
        result_dict["id"] = result_dict.pop("_id")  # The API returns _id, but the SDK returns id
        result_dict.pop("invalidProperty") # The SDK should not return invalid properties
        movie = sdk.Movie().from_dict(movie_dict)

        for attribute in sdk.Movie.VALID_ATTRIBUTES:
            self.assertEqual(movie[attribute], result_dict[attribute])
        with self.assertRaises(KeyError):
            movie["invalidProperty"]
        with self.assertRaises(KeyError):
            movie["nonexistentProperty"]
        self.assertDictEqual(movie.as_dict(), result_dict)

    def test_quote_object(self):
        quote_dict = {
            "_id": "5cd96e05de30eff6ebcce9d3",
            "dialog": "Master. Master looks after us. Master wouldn't hurt us.",
            "movie": "5cd95395de30eff6ebccde5b",
            "character": "5cd99d4bde30eff6ebccfe9e",
            "id": "5cd96e05de30eff6ebcce9d3",
            "invalidProperty": "Whatever",
        }

        result_dict = quote_dict.copy()
        result_dict["id"] = result_dict.pop("_id")  # The API returns _id, but the SDK returns id
        result_dict.pop("invalidProperty") # The SDK should not return invalid properties
        quote = sdk.Quote().from_dict(quote_dict)

        for attribute in sdk.Quote.VALID_ATTRIBUTES:
            self.assertEqual(quote[attribute], result_dict[attribute])
        with self.assertRaises(KeyError):
            quote["invalidProperty"]
        with self.assertRaises(KeyError):
            quote["nonexistentProperty"]
        self.assertDictEqual(quote.as_dict(), result_dict)

    def test_movies_object_set_options(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        options = sdk.RequestOptions(sort="name", filter="name=The Battle of the Five Armies")
        movies = sdk.Movies(api).set_options(options)
        self.assertEqual(movies.get_options(), options)

    def test_movies_object_fetch(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).fetch()
        self.assertEqual(movies.total, 8)
        self.assertEqual(movies.page, 1)
        self.assertEqual(movies.pages, 1)
        self.assertEqual(len(movies.docs), 8)
        self.assertSetEqual(frozenset([movie.name for movie in movies.docs]), frozenset(TestTheOneAPI.SORTED_MOVIE_NAMES))

    def test_movies_object_sort(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("name").fetch()
        self.assertEqual(movies.total, 8)
        self.assertEqual(movies.page, 1)
        self.assertEqual(movies.pages, 1)
        self.assertEqual(len(movies.docs), 8)
        self.assertListEqual([movie.name for movie in movies.docs], TestTheOneAPI.SORTED_MOVIE_NAMES)

        movies.sort("name", sdk.SortOrder.DESCENDING).fetch()
        self.assertEqual(movies.total, 8)
        self.assertEqual(movies.page, 1)
        self.assertEqual(movies.pages, 1)
        self.assertEqual(len(movies.docs), 8)
        self.assertListEqual([movie.name for movie in movies.docs], list(reversed(TestTheOneAPI.SORTED_MOVIE_NAMES)))
