import falcon
import requests

from constant import STATUS_CODE
from authentication import authentication_handler, request_validation


REQUEST_METHOD = {
    "POST": requests.post,
    "GET": requests.get,
    "DELETE": requests.delete,
    "PUT": requests.put,
    "PATCH": requests.patch
}

def payload_handler(response, service_respone):
    response.media = service_respone["data"]
    response.status = STATUS_CODE[service_respone["status_code"]]

def url_processor(url, query, parameter):

    service_url = url

    for param in parameter.keys():
        service_url = service_url.replace("{" + param + "}", parameter[param])

    if query == "":
        return service_url
    return service_url + "?" + query

def data_processor(request):

    data = {}
    files = {}

    for key in request.params.keys():
        if type(request.params.get(key)) is not str:
            files[key] = request.params.get(key).file
        else:
            data[key] = request.params.get(key)

    return data, files




def request_handler(url, request, jwt_secure, parameter):

    query = request.query_string
    service_url = url_processor(url, query, parameter)
    data, files = data_processor(request)
    is_authorize, auth_header = authentication_handler(request, jwt_secure)
    is_save = request_validation(request, url)

    headers = {
        'Authorization': auth_header
    }

    if is_save and is_authorize:
        try:
            response = REQUEST_METHOD[request.method](service_url, data=data, files=files, headers=headers)

            return {
                "data": response.json(),
                "status_code": response.status_code
            }
        except Exception as error:
            raise falcon.HTTPGatewayTimeout(title="Service Error", description=str(error))
    
    return None
        
