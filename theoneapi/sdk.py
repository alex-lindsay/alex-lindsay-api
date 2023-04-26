from typing import TypeVar, Generic, Union
import requests
import pprint

T = TypeVar("T")


class TheOneApiBase:
    """
    Base class for objects that will be retrived using TheOneApi

    Attributes
    ----------
    api : TheOneApi
        The TheOneApi object that was used to make the request.
    options : RequestOptions
        The RequestOptions object that was used to make the request.
    docs : list[T]
        The list of objects returned by the request.
    total : int
        The total number of movies in the database.
    limit : int
        The number of movies per page.
    offset : int
        The number of movies to skip before returning results.
    page : int
        The page number of the results.
    pages : int
        The total number of pages of results.
    """


class TheOneApiDocBase:
    """
    Base class for individual document objects that will be retrived using TheOneApi.

    Attributes
    ----------
    VALID_ATTRIBUTES : list[str]
        A list of the valid attributes for the object.

    Methods
    -------
    from_dict(data: dict) -> T
        Updates the attributes of the object with the values from the data dict.

    asdict() -> dict
        Returns a dictionary of the object's attributes.
    """

    def __init__(self) -> None:
        self.VALID_ATTRIBUTES = []

    def __getitem__(self, key: str) -> Union[str, int, float]:
        """
        Returns the value of the attribute with the given key.

        Parameters
        ----------
        key : str
            The name of the attribute to return the value of.

        Returns
        -------
        Union[str,int,float]
            The value of the attribute with the given key.
        """

        if key not in self.VALID_ATTRIBUTES:
            raise KeyError(f"{key} is not a valid attribute for this object.")

        return self.__dict__[key]

    def as_dict(self) -> dict:
        """
        Returns a dictionary of the object's attributes.

        Returns
        -------
        dict
            A dictionary of the object's attributes.
            Excludes the list of valid attributes.
        """

        return {k:v for (k, v) in self.__dict__.items() if k in self.VALID_ATTRIBUTES}

    def from_dict(self, data: dict) -> "TheOneApiDocBase":
        """
        Updates the attributes of the Movie object with the values from the data dict.

        Parameters
        ----------
        data : dict
            A dictionary of key/value pairs to update the Movie object with.
        """

        
        self.__dict__.update(
            {k: v for (k, v) in data.items() if k in self.VALID_ATTRIBUTES}
        )
        if "_id" in data.keys():
            self.id = data["_id"]
        return self


class Movie(TheOneApiDocBase):
    """
    A structure for representing a movie's data returned from the-one-api.dev.

    Attributes
    ----------
    id : str
        The unique identifier for the movie.
    name : str
        The name of the movie.
    runtimeInMinutes : int
        The runtime of the movie in minutes.
    budgetInMillions : float
        The budget of the movie in millions of dollars.
    boxOfficeRevenueInMillions : float
        The box office revenue of the movie in millions of dollars.
    academyAwardNominations : int
        The number of academy award nominations for the movie.
    academyAwardWins : int
        The number of academy award wins for the movie.
    rottenTomatesScore : int
        The rotten tomatoes score for the movie.
    """

    def __init__(self) -> None:
        super().__init__()
        self.VALID_ATTRIBUTES = [
            "id",
            "name",
            "runtimeInMinutes",
            "budgetInMillions",
            "boxOfficeRevenueInMillions",
            "academyAwardNominations",
            "academyAwardWins",
            "rottenTomatesScore",
        ]


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
        TODO - The number of results to skip before returning results. Default is None.
    sort : str
        A fields to sort by. Default is None.
        An optional leading + on a field name makes it ascending.
        An leading - on a field name makes it descending.
    filter : str
        For now, this is a mongoDB query string. Default is None.

    Methods
    -------
    url_with_query(url: str)
        Returns the url with the query options included as a query string.
    """

    def __init__(
        self,
        limit: int = None,
        page: int = None,
        # offset: int = None,
        sort: str = None,
        filter: str = None,
    ) -> None:
        """
        Parameters
        ----------
        limit : int
            The number of results to return per page. Default is none.
        page : int
            The page number to return. Default is None.
        offset : int
            TODO - The number of results to skip before returning results. Default is None.
        sort : str
            A field name to sort by. Default is None.
            An optional leading + on a field name makes it ascending.
            An leading - on a field name makes it descending.
        filter : str
            For now, this is a mongoDB query string. Default is None.
        """

        self.limit = limit
        self.page = page
        # self.offset = offset
        self.sort = sort
        self.filter = filter

    def url_with_query(self, url: str) -> str:
        """
        Returns the url with the query options included as a query string.

        For each of the defined options, if the option is not None, then add an appropriate part of the query string.
        Join all the parts with a '&' and include a '?' at the beginning as needed and return the resultant url.

        Parameters
        ----------
        url : str
            The url to add the query options to.

        Returns
        -------
        str
            The url with the query options included as a query string.
        """

        url_option_strings = []

        if self.limit is not None:
            url_option_strings.append("limit=" + str(self.limit))
        if self.page is not None:
            url_option_strings.append("page=" + str(self.page))
        # if self.offset is not None:
        #     url_option_strings.append("offset=" + str(self.offset))
        if self.sort is not None:
            if self.sort[0] == "-":
                self.sort = self.sort[1:] + ":desc"
            elif self.sort[0] == "+":
                self.sort = self.sort[1:] + ":asc"
            else:
                self.sort = self.sort + ":asc"
            url_option_strings.append("sort=" + self.sort)
        if self.filter is not None:
            url_option_strings.append(self.filter)

        return (
            len(url_option_strings) > 0
            and url + "?" + "&".join(url_option_strings)
            or url
        )


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
    movies(options: RequestOptions = None)
        Returns a list of movies (paginated, sorted, or filtered) from The One API based on the provided options.
    """

    BASE_URL = "https://the-one-api.dev/v2/"

    def __init__(self, api_key) -> None:
        """
        Parameters
        ----------
        api_key : str
            The API key to use when making requests to The One API
        """

        self._api_key = api_key

    def movies(self, options: RequestOptions = None) -> dict:
        """
        Returns a list of movies (paginated, sorted, or filtered) from The One API based on the provided options.

        Parameters
        ----------
        options : RequestOptions
            The options to use when making the request. Default is None.

        Returns
        -------
        list[dict]
            A list of movies from The One API based on the provided options.

        """

        url = self.BASE_URL + "movie"
        url = options and options.url_with_query(url) or url
        headers = {"Authorization": "Bearer " + self._api_key}
        pprint.pprint(url)
        response = requests.get(url, headers=headers)
        pprint.pprint(response)
        return response.json()
