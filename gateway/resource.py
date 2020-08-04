# Let's get this party started!
import falcon
import requests

from .handler import *
# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class GatewayResource(object):

    service_url = None
    jwt_secure = False

    
    def __init__(self, service_url, jwt_secure):
        self.service_url = service_url
        self.jwt_secure = jwt_secure
    
    def on_get(self, request, response, **kwargs):
        response_service = request_handler(self.service_url, request, self.jwt_secure, kwargs)
        payload_handler(response, response_service)

    def on_post(self, request, response, **kwargs):
        response_service = request_handler(self.service_url, request, self.jwt_secure, kwargs)
        payload_handler(response, response_service)

    def on_delete(self, request, response, **kwargs):
        response_service = request_handler(self.service_url, request, self.jwt_secure, kwargs)
        payload_handler(response, response_service)

    def on_put(self, request, response, **kwargs):
        response_service = request_handler(self.service_url, request, self.jwt_secure, kwargs)
        payload_handler(response, response_service)

    def on_patch(self, request, response, **kwargs):
        response_service = request_handler(self.service_url, request, self.jwt_secure, kwargs)
        payload_handler(response, response_service)
        
