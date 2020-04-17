import requests
import validators

class healthService():
    def __init__(self, baseUrl = None, route = None):
        self.baseUrl = baseUrl
        self.route = route
    
    def post(self, healthJson):
        url = self.baseUrl + self.route
        if validators.url(url) and url != None:
            return (requests.post(url, json=healthJson), None)
        else :
            return (None, -1)