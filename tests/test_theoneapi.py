import unittest
from theoneapi import sdk

VALID_API_KEY = '***REMOVED***'
INVALID_API_KEY = 'FOO'

class TestTheOneAPI(unittest.TestCase):
    def test_init(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        self.assertEqual(api._api_key, VALID_API_KEY)
        self.assertEqual(api.BASE_URL, 'https://the-one-api.dev/v2/')

    def test__add_options_to_url(self):
        api = sdk.TheOneApi(VALID_API_KEY)
        options = sdk.RequestOptions(limit=10, page=1, offset=0, sort='name', filter='{"name":"Gandalf"}')
        url = api._add_options_to_url(api.BASE_URL + 'movie', options)
        self.assertEqual(url, 'https://the-one-api.dev/v2/movie?limit=10&page=1&offset=0&sort=name&filter={"name":"Gandalf"}')
