import requests 
from datetime import datetime

class HTTPSwitcher : 

    def __init__(self, request) :

        """
        Attributes : 
        - request : request sent to the server of the website (attribute of the requests class)
        - status_codes : associates the HTTP response codes to their meaning (hashmap)
        """
        
        self.request = request 
        self.status_codes = {
                            100 : 'Continue',
                            101 : 'Switching protocols',
                            200 : 'OK',
                            201 : 'Created',
                            202 : 'Accepted',
                            203 : 'Non-Authorized information',
                            204 : 'No content',
                            205 : 'Reset content',
                            206 : 'Partial content',
                            301 : 'Moved permanently',
                            302 : 'Moved temporarily',
                            303 : 'See other',
                            304 : 'Not modified',
                            305 : 'Use proxy',
                            310 : 'Too many redirects',
                            400 : 'Bad request',
                            401 : 'Unauthorized',
                            403 : 'Forbidden',
                            404 : 'Not found',
                            405 : 'Method not allowed',
                            408 : 'Request time-out',
                            410 : 'Gone',
                            500 : 'Internal server error',
                            501 : 'Not implemented',
                            502 : 'Bad gateway',
                            503 : 'Service unavailable',
                            504 : 'Gateway time-out'
        } 

    def status(self) : 

        """
        Returns a string which describes the connection status in the status_codes hashmap and the corresponding response code 
        """

        return self.status_codes[self.request.status_code], self.request.status_code


        
