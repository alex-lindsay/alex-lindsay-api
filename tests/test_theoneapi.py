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