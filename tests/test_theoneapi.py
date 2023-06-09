import time
import unittest
from theoneapi import sdk
from decouple import config

VALID_API_KEY = config("THEONEAPI_API_KEY")
INVALID_API_KEY = "FOO"

class TestTheOneAPI(unittest.TestCase):

    def tearDown(self):
        time.sleep(20)

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

    def test_movies_offset(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        options = sdk.RequestOptions(sort="-academyAwardWins", limit=4, page=2, offset=2)
        movies = api.movies(options=options)
        self.assertIn("docs", movies)
        self.assertEqual(movies["total"], 8)
        self.assertEqual(movies["offset"], 2)
        self.assertNotIn("page", movies)
        self.assertEqual(len(movies["docs"]), 4)
        self.assertEqual([movie["academyAwardWins"] for movie in movies["docs"]], [4, 2, 1, 1])

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

    def test_movie(self):
        api = sdk.TheOneApi(INVALID_API_KEY)
        movies = api.movie("5cd95395de30eff6ebccde5b")
        self.assertIn("message", movies)
        self.assertEqual(movies["message"], "Unauthorized.")

        api = sdk.TheOneApi(VALID_API_KEY)
        movies = api.movie("5cd95395de30eff6ebccde5b")
        self.assertIn("docs", movies)
        self.assertEqual(movies["total"], 1)
        self.assertEqual(movies["limit"], 1000)
        self.assertEqual(movies["offset"], 0)
        self.assertEqual(movies["page"], 1)
        self.assertEqual(movies["pages"], 1)
        self.assertEqual(len(movies["docs"]), 1)
        self.assertEqual([movie["name"] for movie in movies["docs"]], ["The Two Towers"])


    def test_quotes(self):
        api = sdk.TheOneApi(INVALID_API_KEY)
        quotes = api.quotes()
        self.assertIn("message", quotes)
        self.assertEqual(quotes["message"], "Unauthorized.")

        api = sdk.TheOneApi(VALID_API_KEY)
        quotes = api.quotes()
        self.assertIn("docs", quotes)
        self.assertEqual(quotes["total"], 2384) # From Postman api test call 4/27/23
        self.assertEqual(quotes["limit"], 1000) # Default limit
        self.assertEqual(quotes["offset"], 0)
        self.assertEqual(quotes["page"], 1)
        self.assertEqual(quotes["pages"], 3)


    def test_quote(self):
        specific_quote = {
            "_id": "5cd96e05de30eff6ebccebd0",
            "dialog": "Get the wounded on horses. The wolves of Isengard will return. Leave the dead.",
            "movie": "5cd95395de30eff6ebccde5b",
            "character": "5cd99d4bde30eff6ebccfe19",
            "id": "5cd96e05de30eff6ebccebd0"
        }
        api = sdk.TheOneApi(INVALID_API_KEY)
        quotes = api.quote("5cd96e05de30eff6ebccebd0")
        self.assertIn("message", quotes)
        self.assertEqual(quotes["message"], "Unauthorized.")

        api = sdk.TheOneApi(VALID_API_KEY)
        quotes = api.quote("5cd96e05de30eff6ebccebd0")
        self.assertIn("docs", quotes)
        self.assertEqual(quotes["total"], 1)
        self.assertEqual(quotes["limit"], 1000)
        self.assertEqual(quotes["offset"], 0)
        self.assertEqual(quotes["page"], 1)
        self.assertEqual(quotes["pages"], 1)
        self.assertEqual(len(quotes["docs"]), 1)
        self.assertDictEqual(quotes["docs"][0], specific_quote)


    def test_movie_quotes(self):
        specific_quote = {
            "_id": "5cd96e05de30eff6ebcce9d6",
            "dialog": "\"Samwise the Brave.\"",
            "movie": "5cd95395de30eff6ebccde5b",
            "character": "5cd99d4bde30eff6ebccfd0d",
            "id": "5cd96e05de30eff6ebcce9d6"
        }
        api = sdk.TheOneApi(INVALID_API_KEY)
        quotes = api.movie_quotes("5cd95395de30eff6ebccde5b")
        self.assertIn("message", quotes)
        self.assertEqual(quotes["message"], "Unauthorized.")

        api = sdk.TheOneApi(VALID_API_KEY)
        options = sdk.RequestOptions(sort="dialog")
        quotes = api.movie_quotes("5cd95395de30eff6ebccde5b", options)
        self.assertIn("docs", quotes)
        self.assertEqual(quotes["total"], 1009)
        self.assertEqual(quotes["limit"], 1000)
        self.assertEqual(quotes["offset"], 0)
        self.assertEqual(quotes["page"], 1)
        self.assertEqual(quotes["pages"], 2)
        self.assertEqual(len(quotes["docs"]), 1000)
        self.assertDictEqual(quotes["docs"][1], specific_quote)



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
        movie = sdk.Movie().from_dict(None, movie_dict)

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
        quote = sdk.Quote().from_dict(None, quote_dict)

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
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], 1)
        self.assertEqual(movies.metadata["pages"], 1)
        self.assertEqual(len(movies.docs), 8)
        self.assertSetEqual(frozenset([movie.name for movie in movies.docs]), frozenset(TestTheOneAPI.SORTED_MOVIE_NAMES))

    def test_movies_object_sort(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("name").fetch()
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], 1)
        self.assertEqual(movies.metadata["pages"], 1)
        self.assertEqual(len(movies.docs), 8)
        self.assertListEqual([movie.name for movie in movies.docs], TestTheOneAPI.SORTED_MOVIE_NAMES)

        movies.sort("name", sdk.SortOrder.DESCENDING).fetch()
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], 1)
        self.assertEqual(movies.metadata["pages"], 1)
        self.assertEqual(len(movies.docs), 8)
        self.assertListEqual([movie.name for movie in movies.docs], list(reversed(TestTheOneAPI.SORTED_MOVIE_NAMES)))

    def test_movies_object_limit(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("name").limit(3).fetch()
        self.assertEqual(movies.metadata["limit"], 3)
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], 1)
        self.assertEqual(movies.metadata["pages"], 3)
        self.assertEqual(len(movies.docs), 3)
        self.assertListEqual([movie.name for movie in movies.docs], TestTheOneAPI.SORTED_MOVIE_NAMES[0:3])

        movies.sort("name", sdk.SortOrder.DESCENDING).fetch()
        self.assertEqual(movies.metadata["limit"], 3)
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], 1)
        self.assertEqual(movies.metadata["pages"], 3)
        self.assertEqual(len(movies.docs), 3)
        self.assertListEqual([movie.name for movie in movies.docs], list(reversed(TestTheOneAPI.SORTED_MOVIE_NAMES))[0:3])

    def test_movies_object_page(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("name").limit(3).page(2).fetch()
        self.assertEqual(movies.metadata["limit"], 3)
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], 2)
        self.assertEqual(movies.metadata["pages"], 3)
        self.assertEqual(len(movies.docs), 3)
        self.assertListEqual([movie.name for movie in movies.docs], TestTheOneAPI.SORTED_MOVIE_NAMES[3:6])

        movies.sort("name", sdk.SortOrder.DESCENDING).fetch()
        self.assertEqual(movies.metadata["limit"], 3)
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], 2)
        self.assertEqual(movies.metadata["pages"], 3)
        self.assertEqual(len(movies.docs), 3)
        self.assertListEqual([movie.name for movie in movies.docs], list(reversed(TestTheOneAPI.SORTED_MOVIE_NAMES))[3:6])

    def test_movies_object_offset(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("academyAwardWins", sdk.SortOrder.DESCENDING).limit(4).offset(2).fetch()
        self.assertEqual(movies.metadata["limit"], 4)
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], None)
        self.assertEqual(movies.metadata["pages"], None)
        self.assertEqual(len(movies.docs), 4)
        self.assertListEqual([movie.academyAwardWins for movie in movies.docs], [4, 2, 1, 1])

        movies = sdk.Movies(api).sort("academyAwardWins", sdk.SortOrder.DESCENDING).limit(4).offset(100).fetch()
        self.assertEqual(movies.metadata["limit"], 4)
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], None)
        self.assertEqual(movies.metadata["pages"], None)
        self.assertEqual(len(movies.docs), 0)
        self.assertListEqual([movie.academyAwardWins for movie in movies.docs], [])

    def test_movies_object_next_page(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("name").limit(3).fetch().next_page()
        self.assertEqual(movies.metadata["limit"], 3)
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], 2)
        self.assertEqual(movies.metadata["pages"], 3)
        self.assertEqual(len(movies.docs), 3)
        self.assertListEqual([movie.name for movie in movies.docs], TestTheOneAPI.SORTED_MOVIE_NAMES[3:6])

        movies.next_page()
        self.assertEqual(movies.metadata["limit"], 3)
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], 3)
        self.assertEqual(movies.metadata["pages"], 3)
        self.assertEqual(len(movies.docs), 2)
        self.assertListEqual([movie.name for movie in movies.docs], TestTheOneAPI.SORTED_MOVIE_NAMES[6:8])

        movies.next_page()
        self.assertEqual(movies.metadata["limit"], 3)
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], 4)
        self.assertEqual(movies.metadata["pages"], 3)
        self.assertEqual(len(movies.docs), 0)
        self.assertListEqual([movie.name for movie in movies.docs], [])

    def test_movies_object_previous_page(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("name").limit(3).page(2).fetch().previous_page()
        self.assertEqual(movies.metadata["limit"], 3)
        self.assertEqual(movies.metadata["total"], 8)
        self.assertEqual(movies.metadata["page"], 1)
        self.assertEqual(movies.metadata["pages"], 3)
        self.assertEqual(len(movies.docs), 3)
        self.assertListEqual([movie.name for movie in movies.docs], TestTheOneAPI.SORTED_MOVIE_NAMES[0:3])

        # TODO - moving back beyond page 1 is misbehaving
        # movies.previous_page()
        # self.assertEqual(movies.metadata["limit"], 2)
        # self.assertEqual(movies.metadata["total"], 8)
        # self.assertEqual(movies.metadata["page"], 1)
        # self.assertEqual(movies.metadata["pages"], 3)
        # self.assertEqual(len(movies.docs), 3)
        # self.assertListEqual([movie.name for movie in movies.docs], [])

        # movies.previous_page()
        # self.assertEqual(movies.metadata["limit"], 3)
        # self.assertEqual(movies.metadata["total"], 8)
        # self.assertEqual(movies.metadata["page"], None)
        # self.assertEqual(movies.metadata["pages"], None)
        # self.assertEqual(len(movies.docs), 0)
        # self.assertListEqual([movie.name for movie in movies.docs], [])

    def test_movies_object_filter(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("name").filter("name=The Return of the King").fetch()
        self.assertEqual(movies.metadata["limit"], 1000) # Default limit
        self.assertEqual(movies.metadata["total"], 1)
        self.assertEqual(movies.metadata["page"], 1)
        self.assertEqual(movies.metadata["pages"], 1)
        self.assertEqual(len(movies.docs), 1)
        self.assertListEqual([movie.name for movie in movies.docs], ["The Return of the King"])

        # Only the second filter should take effect
        movies = sdk.Movies(api).sort("name").filter("budgetInMillions<100").filter("runtimeInMinutes>=400").fetch()
        self.assertEqual(movies.metadata["limit"], 1000) # Default limit
        self.assertEqual(movies.metadata["total"], 2)
        self.assertEqual(movies.metadata["page"], 1)
        self.assertEqual(movies.metadata["pages"], 1)
        self.assertEqual(len(movies.docs), 2)
        self.assertSetEqual(frozenset([movie.runtimeInMinutes for movie in movies.docs]), frozenset([558, 462]))

    def test_movies_object_match(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).match("name", "The Return of the King").fetch()
        self.assertEqual(movies.metadata["limit"], 1000)
        self.assertListEqual([movie.name for movie in movies.docs], ["The Return of the King"])

        movies = sdk.Movies(api).match("name", "The Return of the King", True).fetch()
        self.assertEqual(movies.metadata["limit"], 1000)
        self.assertEqual(len(movies.docs), 7)
        self.assertNotIn("The Return of the King", [movie.name for movie in movies.docs])

        movies = sdk.Movies(api).match("names", "The Return of the King").fetch()
        self.assertEqual(movies.metadata["limit"], 1000)
        self.assertListEqual([movie.name for movie in movies.docs], [])

    def test_movies_object_include(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("academyAwardNominations", sdk.SortOrder.DESCENDING).include("academyAwardNominations", [13,11,7]).fetch()
        self.assertEqual(len(movies.docs), 3)
        self.assertListEqual([movie.academyAwardWins for movie in movies.docs], [4,11,1])

        movies = sdk.Movies(api).sort("academyAwardNominations", sdk.SortOrder.DESCENDING).include("academyAwardNominations", [13,11,7], True).fetch()
        self.assertEqual(len(movies.docs), 5)
        self.assertListEqual([movie.academyAwardWins for movie in movies.docs], [17,2,1,0,0])

    def test_movies_object_exclude(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("academyAwardNominations", sdk.SortOrder.DESCENDING).exclude("academyAwardNominations", [13,11,7]).fetch()
        self.assertEqual(len(movies.docs), 5)
        self.assertListEqual([movie.academyAwardWins for movie in movies.docs], [17,2,1,0,0])

    def test_movies_object_exists(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).exists("academyAwardNominations").fetch()
        self.assertEqual(len(movies.docs), 8)

        movies = sdk.Movies(api).exists("academyAwardNominations", True).fetch()
        self.assertEqual(len(movies.docs), 0)

    def test_movies_object_regex(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("name").regex("name", "/of the/i").fetch()
        self.assertEqual(len(movies.docs), len(self.SORTED_OF_THE_MOVIE_NAMES))
        self.assertListEqual([movie.name for movie in movies.docs], self.SORTED_OF_THE_MOVIE_NAMES)

    def test_movies_object_less_than(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("budgetInMillions").less_than("budgetInMillions", 94).fetch()
        self.assertEqual(len(movies.docs), 1)
        self.assertListEqual([movie.budgetInMillions for movie in movies.docs], [93])

        movies = sdk.Movies(api).sort("budgetInMillions").less_than("budgetInMillions", 94, True).fetch()
        self.assertEqual(len(movies.docs), 3)
        self.assertListEqual([movie.budgetInMillions for movie in movies.docs], [93, 94, 94])

    def test_movies_object_greater_than(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).sort("academyAwardWins", sdk.SortOrder.DESCENDING).greater_than("academyAwardWins", 11).fetch()
        self.assertEqual(len(movies.docs), 1)
        self.assertListEqual([movie.name for movie in movies.docs], self.SORTED_BIG_WINNER_MOVIE_NAMES[0:1])

        movies = sdk.Movies(api).sort("academyAwardWins", sdk.SortOrder.DESCENDING).greater_than("academyAwardWins", 11, True).fetch()
        self.assertEqual(len(movies.docs), 2)
        self.assertListEqual([movie.name for movie in movies.docs], self.SORTED_BIG_WINNER_MOVIE_NAMES)

    def test_movies_object_by_id(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        movies = sdk.Movies(api).by_id("5cd95395de30eff6ebccde5b")
        self.assertEqual(len(movies.docs), 1)
        self.assertListEqual([movie.name for movie in movies.docs], ["The Two Towers"])

    def test_quotes_object_fetch(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        quotes = sdk.Quotes(api).sort("dialog").limit(3).page(2).fetch()
        self.assertEqual(quotes.metadata["total"], 2384) # From Postman test API call
        self.assertEqual(quotes.metadata["limit"], 3) # From Postman test API call
        self.assertEqual(quotes.metadata["offset"], None) 
        self.assertEqual(quotes.metadata["page"], 2) # From Postman test API call
        self.assertEqual(quotes.metadata["pages"], 795) # From Postman test API call
        self.assertEqual(len(quotes.docs), 3)
        self.assertDictEqual(quotes.docs[0].as_dict(), {
            # "_id": "5cd96e05de30eff6ebcce825", # _id attribute is merged to id
            "dialog": "\"There and Back Again, a Hobbit's tale\" by Bilbo Baggins and \"The Lord of the Rings\" by Frodo Baggins. You finished it.",
            "movie": "5cd95395de30eff6ebccde5d",
            "character": "5cd99d4bde30eff6ebccfd0d",
            "id": "5cd96e05de30eff6ebcce825"
        })
        self.assertDictEqual(quotes.docs[1].as_dict(), {
            # "_id": "5cd96e05de30eff6ebcceb64", # _id attribute is merged to id
            "dialog": "' i vethed... n' i onnad. Boe bedich go Frodo. Han b'd l'n.",
            "movie": "5cd95395de30eff6ebccde5b",
            "character": "5cd99d4bde30eff6ebccfc07",
            "id": "5cd96e05de30eff6ebcceb64"
        })
        self.assertDictEqual(quotes.docs[2].as_dict(), {
            # "_id": "5cd96e05de30eff6ebcceb7d", # _id attribute is merged to id
            "dialog": "'-bedin o gurth ne dagor.",
            "movie": "5cd95395de30eff6ebccde5b",
            "character": "5cd99d4bde30eff6ebccfbe6",
            "id": "5cd96e05de30eff6ebcceb7d"
        })

    def test_quotes_object_by_id(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        quotes = sdk.Quotes(api).by_id("5cd96e05de30eff6ebcceb7d")
        self.assertEqual(len(quotes.docs), 1)
        self.assertListEqual([quote.dialog for quote in quotes.docs], ["'-bedin o gurth ne dagor."])

