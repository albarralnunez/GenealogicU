import urllib
import os
import json

try:
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
except:
    raise EnvironmentError('GOOGLE_API_KEY envrioment variable not found')

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class Client:  

    def __init__(self, format='json'):

        self.baseURL = 'https://maps.googleapis.com/maps/api/geocode/'
        self.baseURL += format

    def request(request_given):
        
        def new(*args):

            request = args[0].baseURL + request_given(*args) + '&key=' + GOOGLE_API_KEY
            sock = urllib.urlopen(request)
            response = sock.read()
            sock.close()
            json_response = json.loads(response[:-1])
            return json_response

        return new

    @request
    def request_component(self, query):
        request = '?components='
        request += '|'.join([component['types'][0] + ':' + component['short_name'] 
                for component in query])
        return request
