from typing import List, Any, Callable
from urllib.parse import quote, urlparse, ParseResult, parse_qs, urlencode
from json import loads, dumps

from googleapiclient.http import build_http, HttpRequest

class PaginatedResults(object):

    WRAPPER_CLASS : type
    YOUTUBE_CLIENT : Any
    RESPONSE : dict
    REQUEST : Any
    RESOURCE : Any

    CACHED_WRAPPED_ITEMS : List[Any]

    def __init__(
            self,
            yt : Any, 
            req : Any, 
            res : dict,
            resource : Any,
            wrapperClass : type) -> None:

        # The class which the items are meant to be turned into
        self.WRAPPER_CLASS = wrapperClass

        # Passing the youtube client to handle pagination
        self.YOUTUBE_CLIENT = yt

        # The initial json response
        self.RESPONSE = res

        self.REQUEST = req

        self.RESOURCE = resource

        self.CACHED_WRAPPED_ITEMS = None

    def hasNextPage(self) -> None:
        return "nextPageToken" in self.RESPONSE.keys()

    def next(self) -> None:
        """Mutator function which goes to the next page of the query"""

        if "nextPageToken" not in self.RESPONSE.keys():
            raise Exception()

        new_req = self.RESOURCE.list_next(self.REQUEST, self.RESPONSE)
        new_res = new_req.execute()

        self.REQUEST = new_req
        self.RESPONSE = new_res

        # Data is no longer relevant at this point
        self.CACHED_WRAPPED_ITEMS = None

    def get_wrapped_items(self) -> List[Any]:

        if self.CACHED_WRAPPED_ITEMS is None:
            self.CACHED_WRAPPED_ITEMS = [self.WRAPPER_CLASS.construct_from_response(x) for x in self.RESPONSE['items']]

        return self.CACHED_WRAPPED_ITEMS

    def map_to_response(self, f : Callable) -> Any:
        return list( map(f, self.get_wrapped_items()) )
    
    # Double Underscore Methods (Dunder)

    def __iter__(self):
        self.current_index = 0
        return self
    
    def __next__(self):

        n = self.get_wrapped_items() # Generate Wrapped Items if not existed

        if self.current_index < len(n):
            x = n[self.current_index]
            self.current_index += 1
            return x
    
        # normally we would raise StopIteration here
        if self.hasNextPage():      # This is the most confusing thing ever, I'm sorry
            self.next()
            next(self)

        raise StopIteration
    
    def __len__(self):
        return len(self.get_wrapped_items())
    
    def __getitem__(self, k : int):
        return self.get_wrapped_items()[k]