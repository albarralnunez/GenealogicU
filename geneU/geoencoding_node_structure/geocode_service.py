import urllib
import os
import json


GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

class Client():  

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
            if json_response['status'] == '':


            return json_response

        return new

    @request
    def request_component(self, query): 
        request = '?components='
        fst_it = True
        for component in query:
            if fst_it:
                fst_it = False
            else:
                request += '|'
            request += component['types'][0] + ':' + component['short_name']
        return request
