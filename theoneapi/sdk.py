from typing import TypeVar, Generic, Union
from abc import ABC, abstractmethod
from enum import Enum
import requests


class SortOrder(Enum):
    ASCENDING = "+"
    DESCENDING = "-"


class TheOneApiBase(ABC):
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
    metadata : dict
        A dictionary of metadata returned by the request.
    metadata.total : int
        The total number of movies in the database.
    metadata.limit : int
        The number of movies per page.
    metadata.offset : int
        The number of movies to skip before returning results.
    metadata.page : int
        The page number of the results.
    metadata.pages : int
        The total number of pages of results.

    Methods
    -------
    set_options(options: RequestOptions) -> None
        Sets the options attribute to the given RequestOptions object.

    get_options() -> RequestOptions
        Returns the RequestOptions object used to make the request.

    get_metadata() -> RequestOptions
        Returns the metadata values based on the last request.

    fetch() -> TheOneApiBase
        Fetches the data from the API using the given options and returns the object for chaining.

    sort(field: str, order: SortOrder = ASCENDING) -> TheOneApiBase
        Sets the sort option to the given field, marking it as ascending as needed and returns the object for chaining.

    limit(limit: int) -> TheOneApiBase
        Sets the limit option to the given value and returns the object for chaining.

    page(page: int) -> TheOneApiBase
        Sets the page option to the given value and returns the object for chaining.

    offset(offset: int) -> TheOneApiBase
        Sets the offset option to the given value and returns the object for chaining.

    next_page() -> TheOneApiBase
        Fetches the next page of results and returns the object for chaining.

    previous_page() -> TheOneApiBase
        Fetches the previous page of results and returns the object for chaining.

    filter(filter: str) -> TheOneApiBase
        Sets the filter option to the given value and returns the object for chaining.

    match(field: str, value: Union[str, int, float], negate: bool = False) -> TheOneApiBase
        Sets the filter option to a string for matching the given field to the given value and returns the object for chaining.

    include(field: str, values: list(Union[str, int, float]), negate: bool = False) -> TheOneApiBase
        Sets the filter option to a string for matching the given field to any of the given values and returns the object for chaining.

    exclude(field: str, values: list(Union[str, int, float])) -> TheOneApiBase
        Sets the filter option to a string for matching the given field to anything not one of the given values and returns the object for chaining.
        This is a convenience method that calls include with the negate parameter set to True.

    exists(field: str, negate: boolean = False) -> TheOneApiBase
        Sets the filter option to a string for matching if the given field exists (or doesn't exist, based on the negate parameter) and returns the object for chaining.

    regex(field: str, pattern: str, negate: boolean = False) -> TheOneApiBase
        Sets the filter option to a string for matching the given field to the given regular expression pattern (or the inverse, based on the negate parameter) and returns the object for chaining.

    lessThan(field: str, value: Union[str, int, float], orEqual: boolean = False) -> TheOneApiBase
        Sets the filter option to a string for matching the given field to values less than (or optionally equal to) the given value and returns the object for chaining.

    greaterThan(field: str, value: Union[str, int, float], orEqual: boolean = False) -> TheOneApiBase
        Sets the filter option to a string for matching the given field to values greater than (or optionally equal to) the given value and returns the object for chaining.

    by_id(id: str) -> TheOneApiBase
        Get a specific document from the collection based on the idea and returns the collection object for chaining.
    """

    METADATA_FIELDS = ["total", "limit", "offset", "page", "pages"]

    def __init__(self, api: "TheOneApi", options: "RequestOptions" = None) -> None:
        self.api = api
        self.options = options is not None and options or RequestOptions()
        self.docs = []
        self.metadata = {"total": 0, "limit": 0, "offset": 0, "page": 0, "pages": 0}

    def set_metadata(self, data: dict) -> "TheOneApiBase":
        """
        Updates the attributes of the Base object with the values from the data dict.
        Child classes are expected to convert the docs list into a list of BaseDoc objects.

        Parameters
        ----------
        data : dict
            A dictionary of key/value pairs to update the Movies object with.
        """

        metadata = [(k, k in data and data[k] or None) for k in self.METADATA_FIELDS]
        self.metadata = dict(metadata)
        return self

    def set_options(self, options: "RequestOptions") -> "TheOneApiBase":
        """
        Sets the options attribute to the given RequestOptions object.

        Parameters
        ----------
        options : RequestOptions
            The RequestOptions object to set the options attribute to.
        """

        self.options = options
        return self

    def get_options(self) -> "RequestOptions":
        """
        Returns the options attribute.

        Returns
        -------
        RequestOptions
            The options attribute.
        """

        return self.options

    @abstractmethod
    def fetch(self) -> "TheOneApiBase":  # pragma: no cover
        """
        Fetches the data from the API using the given options and returns the object for chaining.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        pass

    def sort(
        self, field: str, order: SortOrder = SortOrder.ASCENDING
    ) -> "TheOneApiBase":
        """
        Sets the sort option to the given field, marking it as ascending as needed and returns the object for chaining.

        Parameters
        ----------
        sort : str
            The field to sort by.
        ascending : bool, optional
            Whether to sort ascending or descending, by default True

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.sort = order.value + field
        return self

    def limit(self, limit: int) -> "TheOneApiBase":
        """
        Sets the limit option to the given value and returns the object for chaining.

        Parameters
        ----------
        limit : int
            The value to set the limit option to.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.limit = limit
        return self

    def page(self, page: int) -> "TheOneApiBase":
        """
        Sets the page option to the given value and returns the object for chaining.

        Parameters
        ----------
        page : int
            The value to set the page option to.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.page = page
        return self

    def offset(self, offset: int) -> "TheOneApiBase":
        """
        Sets the offset option to the given value and returns the object for chaining.

        Parameters
        ----------
        offset : int
            The value to set the offset option to.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.offset = offset
        return self

    def next_page(self) -> "TheOneApiBase":
        """
        Sets the page option to the next page and returns the object for chaining.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.page = ("page" in self.metadata) and (self.metadata["page"] + 1) or 1
        return self.fetch()
    
    # TODO: There is an error which occurs if page is < 1
    def previous_page(self) -> "TheOneApiBase":
        """
        Sets the page option to the previous page and returns the object for chaining.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.page = ("page" in self.metadata) and (self.metadata["page"] - 1) or 1
        return self.fetch()
    
    def filter(self, filter: str) -> "TheOneApiBase":
        """
        Sets the filter option to a string for matching the given field to the given value and returns the object for chaining.

        Parameters
        ----------
        filter : str
            The string to use as the filter in the query.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.filter = f"{filter}"
        return self
    
    def match(self, field: str, value: Union[str, int, float], negate: bool = False) -> "TheOneApiBase":
        """
        Sets the filter option to a string for matching the given field to the given value and returns the object for chaining.

        Parameters
        ----------
        field : str
            The field to match.
        value : Union[str,int,float]
            The value to match the field to.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.filter = f"{field}{negate and '!' or ''}={value}"
        return self
    
    def include(self, field: str, values: list[Union[str, int, float]], negate: bool = False) -> "TheOneApiBase":
        """
        Sets the include option to a string for matching the given field to the given values and returns the object for chaining.

        Parameters
        ----------
        field : str
            The field to match.
        values : list[Union[str,int,float]]
            The values to match the field to.
        negate : bool, optional
            Whether to negate the match, by default False

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.filter = f"{field}{negate and '!' or ''}={','.join(map(str,values))}"
        return self
    
    def exclude(self, field: str, values: list[Union[str, int, float]]) -> "TheOneApiBase":
        """
        Sets the exclude option to a string for matching the given field to the given values and returns the object for chaining.

        Parameters
        ----------
        field : str
            The field to match.
        values : list[Union[str,int,float]]
            The values to match the field to.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        return self.include(field, values, True)
    
    def exists(self, field: str, negate: bool = False) -> "TheOneApiBase":
        """
        Sets the filter option to a string for matching the given field to the given values and returns the object for chaining.

        Parameters
        ----------
        field : str
            The field to match.
        negate : bool, optional
            Whether to negate the match, by default False

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.filter = f"{negate and '!' or ''}{field}"
        return self
    
    def regex(self, field: str, regex: str, negate: bool = False) -> "TheOneApiBase":
        """
        Sets the filter option to a string for matching the given field to the given regex and returns the object for chaining.

        Parameters
        ----------
        field : str
            The field to match.
        regex : str
            The regex to match the field to.
        negate : bool, optional
            Whether to negate the match, by default False

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.filter = f"{field}{negate and '!' or ''}={regex}"
        return self
    
    def less_than(self, field: str, value: Union[str, int, float], orEqual: bool = False) -> "TheOneApiBase":
        """
        Sets the filter option to a string for matching the given field to a value less than the given value and returns the object for chaining.

        Parameters
        ----------
        field : str
            The field to match.
        value : Union[str,int,float]
            The value to match the field to.
        orEqual : bool, optional

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.filter = f"{field}<{orEqual and '=' or ''}{value}"
        return self
    
    def greater_than(self, field: str, value: Union[str, int, float], orEqual: bool = False) -> "TheOneApiBase":
        """
        Sets the filter option to a string for matching the given field to a value greater than the given value and returns the object for chaining.

        Parameters
        ----------
        field : str
            The field to match.
        value : Union[str,int,float]
            The value to match the field to.
        orEqual : bool, optional

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.options.filter = f"{field}>{orEqual and '=' or ''}{value}"
        return self


class TheOneApiDocBase:
    """
    Base class for individual document objects that will be retrived using TheOneApi.

    Attributes
    ----------
    VALID_ATTRIBUTES : list[str]
        A list of the valid attributes for the object.

    api : TheOneApi
        The TheOneApi object that was used to make the request.

    Methods
    -------
    from_dict(api: TheOneApi, data: dict) -> T
        Updates the attributes of the object with the values from the data dict.

    asdict() -> dict
        Returns a dictionary of the object's attributes.
    """

    VALID_ATTRIBUTES = []

    def __init__(self) -> None:
        pass

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

        return {k: v for (k, v) in self.__dict__.items() if k in self.VALID_ATTRIBUTES}

    def from_dict(self, api: "TheOneApi", data: dict) -> "TheOneApiDocBase":
        """
        Updates the attributes of the Movie object with the values from the data dict.

        Parameters
        ----------
        api : TheOneApi
            The TheOneApi object that was used to make the request.
        data : dict
            A dictionary of key/value pairs to update the Movie object with.
        """

        self.api = api
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
        The rotten tomatoes score for the movie.'

    Methods
    -------
    quotes() -> Quotes
        Returns a Quotes object for the given Movie.
    """

    VALID_ATTRIBUTES = [
        "id",
        "name",
        "runtimeInMinutes",
        "budgetInMillions",
        "boxOfficeRevenueInMillions",
        "academyAwardNominations",
        "academyAwardWins",
        "rottenTomatesScore",
    ]

    def __init__(self) -> None:
        super().__init__()

    def quotes(self) -> "Quotes":
        """
        Returns a Quotes object for the given Movie.

        Returns
        -------
        Quotes
            A Quotes object for the given Movie.
        """

        return Quotes(self.api).match("movie", self.id).fetch()


class Quote(TheOneApiDocBase):
    """
    A structure for representing a quote's data returned from the-one-api.dev.

    Attributes
    ----------
    id : str
        The unique identifier for the quote.
    dialog : str
        The dialog of the quote.
    movie : str
        The unique identifier for the movie the quote is from.
    character : str
        The unique identifier for the movie the quote is from.
    """

    VALID_ATTRIBUTES = ["id", "dialog", "movie", "character"]

    def __init__(self) -> None:
        super().__init__()


class Movies(TheOneApiBase):
    """
    A class for retrieving a list of movies from the-one-api.dev and representing them as a list of Movie objects.

    Attributes
    ----------
    docs : list[Movie]
        The list of Movie objects returned by the request.
    """

    def __init__(self, api: "TheOneApi", options: "RequestOptions" = None) -> None:
        super().__init__(api, options)

    # TODO: Error handling - sending a page number of 0 or less returns an error message JSON
    def fetch(self) -> "Movies":
        """
        Fetches movie data from the API using the given options and returns the object for chaining.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.docs = []
        data = self.api.movies(self.options)
        super().set_metadata(data)

        if "docs" in data:
            self.docs = [Movie().from_dict(self.api, movie) for movie in data["docs"]]

        return self
    
    def by_id(self, id: str) -> "Movies":
        """
        Gets a specific movie by id.

        Parameters
        ----------
        id : str
            The id to match.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.docs = []
        data = self.api.movie(id)
        super().set_metadata(data)
        # TODO - there's probably more work to be done here to reset the RequestOptions in an ideal way
        self.match("_id", id)

        if "docs" in data:
            self.docs = [Movie().from_dict(self.api, movie) for movie in data["docs"]]

        return self


class Quotes(TheOneApiBase):
    """
    A class for retrieving a list of quotes from the-one-api.dev and representing them as a list of Quote objects.

    Attributes
    ----------
    docs : list[Quote]
        The list of Quote objects returned by the request.
    """

    def __init__(self, api: "TheOneApi", options: "RequestOptions" = None) -> None:
        super().__init__(api, options)

    def fetch(self) -> "Quotes":
        """
        Fetches quote data from the API using the given options and returns the object for chaining.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.docs = []
        data = self.api.quotes(self.options)
        super().set_metadata(data)

        if "docs" in data:
            self.docs = [Quote().from_dict(self.api, quote) for quote in data["docs"]]

        return self

    def by_id(self, id: str) -> "Quotes":
        """
        Gets a specific quote by id.

        Parameters
        ----------
        id : str
            The id to match.

        Returns
        -------
        TheOneApiBase
            The object for chaining.
        """

        self.docs = []
        data = self.api.quote(id)
        super().set_metadata(data)

        # TODO - what happens if self.api is None?
        if "docs" in data:
            self.docs = [Quote().from_dict(self.api, quote) for quote in data["docs"]]

        return self


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
        offset: int = None,
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
            The number of results to skip before returning results. Default is None.
        sort : str
            A field name to sort by. Default is None.
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

        if self.offset is not None:
            url_option_strings.append("offset=" + str(self.offset))
        if self.limit is not None:
            url_option_strings.append("limit=" + str(self.limit))
        # If offset is set, page should be ignored.
        if self.page is not None and self.offset is None:
            url_option_strings.append("page=" + str(self.page))
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
    >>> movies = api.movies()
    >>> print(movies.docs[0].name)

    Attributes
    ----------
    api_key : str
        The API key to use when making requests to The One API

    Methods
    -------
    movies(options: RequestOptions = None)
        Returns a list of movies (paginated, sorted, or filtered) from The One API based on the provided options.
    movie(id: str)
        Returns a movie collection containing one movie from The One API based on the provided movie id.
    quotes(options: RequestOptions = None)
        Returns a list of quotes (paginated, sorted, or filtered) from The One API based on the provided options.
    quote(id: str)
        Returns a quote collection containing one movie from The One API based on the provided quote id.
    movie_quotes(id: str)
        Returns a quote collection containing quotes from one movie from The One API based on the provided movie id.
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

        # TODO - Deal with error conditions - get happy path working first
        url = self.BASE_URL + "movie"
        url = options and options.url_with_query(url) or url
        headers = {"Authorization": "Bearer " + self._api_key}
        response = requests.get(url, headers=headers)
        return response.json()

    def movie(self, id: str) -> dict:
        """
        Returns a movie collection containing one movie from The One API based on the provided movie id.

        Parameters
        ----------
        id : str
            The id of the movie to return.

        Returns
        -------
        dict
            A movie from The One API based on the provided movie id.

        """

        # TODO - Deal with error conditions - get happy path working first
        url = self.BASE_URL + "movie/" + id
        headers = {"Authorization": "Bearer " + self._api_key}
        response = requests.get(url, headers=headers)
        return response.json()
    
    def quotes(self, options: RequestOptions = None) -> dict:
        """
        Returns a list of quotes (paginated, sorted, or filtered) from The One API based on the provided options.

        Parameters
        ----------
        options : RequestOptions
            The options to use when making the request. Default is None.

        Returns
        -------
        list[dict]
            A list of quotes from The One API based on the provided options.

        """
            
        # TODO - Deal with error conditions - get happy path working first
        url = f"{self.BASE_URL}quote"
        url = options and options.url_with_query(url) or url
        headers = {"Authorization": "Bearer " + self._api_key}
        response = requests.get(url, headers=headers)
        return response.json()
    
    def quote(self, id: str) -> dict:
        """
        Returns a quote collection containing one quote from The One API based on the provided quote id.

        Parameters
        ----------
        id : str
            The id of the quote to return.

        Returns
        -------
        dict
            A quote from The One API based on the provided quote id.

        """
            
        # TODO - Deal with error conditions - get happy path working first
        url = f"{self.BASE_URL}quote/{id}"
        headers = {"Authorization": "Bearer " + self._api_key}
        response = requests.get(url, headers=headers)
        return response.json()
    
    def movie_quotes(self, id: str, options: RequestOptions = None) -> dict:
        """
        Returns a quote collection containing quotes from one movie from The One API based on the provided movie id.

        Parameters
        ----------
        id : str
            The id of the movie to return quotes for.

        Returns
        -------
        dict
            A quote collection from The One API based on the provided movie id.

        """
        # TODO - Deal with error conditions - get happy path working first
        url = f"{self.BASE_URL}movie/{id}/quote"
        url = options and options.url_with_query(url) or url
        headers = {"Authorization": "Bearer " + self._api_key}
        response = requests.get(url, headers=headers)
        return response.json()