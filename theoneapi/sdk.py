import requests


class RequestOptions:
    """
    A structure for presenting query options when making a request to TheOneApi

    Attributes
    ----------
    limit : int
        The number of results to return per page. Default is 10. None represents no limit.
    page : int
        The page number to return. Default is 1.
    offset : int
        The number of results to skip before returning results. Default is None.
    sort : list[str]
        A list of fields to sort by. Default is None.
        An optional leading + on a field name makes it ascending.
        An leading - on a field name makes it descending.
    filter : str
        For now, this is a mongoDB query string. Default is None.
    """

    def __init__(
        self, limit: int = 10, page: int = 1, offset: int = None, sort=None, filter=None
    ):
        """
        Parameters
        ----------
        limit : int
            The number of results to return per page. Default is 10. None represents no limit.
        page : int
            The page number to return. Default is 1.
        offset : int
            The number of results to skip before returning results. Default is None.
        sort : list[str]
            A list of fields to sort by. Default is None.
            An optional leading + on a field name makes it ascending.
            An leading - on a field name makes it descending.
        filter : str
            For now, this is a mongoDB query string. Default is None.
        """
        self.limit = limit
        self.page = page
        self.offset = offset
        self.sort = sort
        self.filter = filter


class TheOneApi:
    """
    A Python SDK for The One API.

    A simple example of how to use this SDK:
    >>> import theoneapi
    >>> api = theoneapi.TheOneApi('YOUR_API_KEY')
    >>> books = api.books()
    >>> print(books)

    Attributes
    ----------
    api_key : str
        The API key to use when making requests to The One API

    Methods
    -------
    movies(options=None)
        Returns a list of movies (paginated, sorted, or filtered) from The One API based on the provided options.
    """

    BASE_URL = "https://the-one-api.dev/v2/"

    def __init__(self, api_key):
        self._api_key = api_key

    def _add_options_to_url(self, url, options):
        if options is None:
            return url

        url += "?"
        url_option_strings = []

        if options.limit is not None:
            url_option_strings.append("limit=" + str(options.limit))
        if options.page is not None:
            url_option_strings.append("page=" + str(options.page))
        if options.offset is not None:
            url_option_strings.append("offset=" + str(options.offset))
        if options.sort is not None:
            if options.sort[0] == "-":
                options.sort = options.sort[1:] + ":desc"
            url_option_strings.append("sort=" + options.sort)
        if options.filter is not None:
            url_option_strings.append("filter=" + options.filter)

        return url + "&".join(url_option_strings)

    def movies(self, options=None):
        url = self.BASE_URL + "movie"
        headers = {"Authorization": "Bearer " + self._api_key}
        response = requests.get(url, headers=headers)
        return response.json()
